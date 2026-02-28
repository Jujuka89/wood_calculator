from datetime import timedelta, datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.event import async_track_time_interval
from .const import *

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    temp_sensor = config.get("poele_sensor")
    seuil = config.get("temp_seuil", DEFAULT_TEMP_SEUIL)
    duree_buche = config.get("duree_buche", DEFAULT_DUREE_BUCHE)
    buches_stere = config.get("buches_stere", DEFAULT_BUCHES_STERE)
    prix_stere = config.get("prix_stere", DEFAULT_PRIX_STERE)

    # Création tracker
    tracker = WoodTracker(hass, temp_sensor, seuil, duree_buche)

    # Capteurs
    log_sensor = WoodLogsSensor(tracker)
    stere_sensor = WoodStereSensor(tracker, buches_stere)
    cost_sensor = WoodCostSensor(tracker, buches_stere, prix_stere)
    binary_sensor_poele = WoodBinarySensor(tracker)

    async_add_entities([log_sensor, stere_sensor, cost_sensor, binary_sensor_poele])
    tracker.start()


class WoodTracker:
    """Compteur de temps de fonctionnement du poêle"""
    def __init__(self, hass, temp_sensor, seuil, duree_buche):
        self.hass = hass
        self.temp_sensor = temp_sensor
        self.seuil = seuil
        self.duree_buche = duree_buche
        self.minutes_on = 0
        self.last_day = datetime.now().day
        self._binary_state = False

    def start(self):
        async_track_time_interval(
            self.hass,
            self.update,
            timedelta(minutes=1)
        )

    async def update(self, now):
        today = datetime.now().day

        # Reset quotidien
        if today != self.last_day:
            self.minutes_on = 0
            self.last_day = today

        state = self.hass.states.get(self.temp_sensor)
        if state and state.state not in ("unknown", "unavailable"):
            if float(state.state) >= self.seuil:
                self.minutes_on += 1
                self._binary_state = True
            else:
                self._binary_state = False

    @property
    def logs(self):
        return round(self.minutes_on / self.duree_buche, 2)

    @property
    def binary_state(self):
        return self._binary_state


# ----------------------------
# Capteurs
# ----------------------------

class WoodLogsSensor(SensorEntity):
    def __init__(self, tracker):
        self.tracker = tracker
        self._attr_name = "Bûches brûlées (jour)"
        self._attr_native_unit_of_measurement = "bûches"

    @property
    def native_value(self):
        return self.tracker.logs


class WoodStereSensor(SensorEntity):
    def __init__(self, tracker, buches_stere):
        self.tracker = tracker
        self.buches_stere = buches_stere
        self._attr_name = "Consommation Bois (stère)"
        self._attr_native_unit_of_measurement = "st"

    @property
    def native_value(self):
        return round(self.tracker.logs / self.buches_stere, 4)


class WoodCostSensor(SensorEntity):
    def __init__(self, tracker, buches_stere, prix_stere):
        self.tracker = tracker
        self.buches_stere = buches_stere
        self.prix_stere = prix_stere
        self._attr_name = "Coût Bois (jour)"
        self._attr_native_unit_of_measurement = "€"

    @property
    def native_value(self):
        stere = self.tracker.logs / self.buches_stere
        return round(stere * self.prix_stere, 2)


class WoodBinarySensor(BinarySensorEntity):
    """Binary sensor pour poêle en route"""
    def __init__(self, tracker):
        self.tracker = tracker
        self._attr_name = "Poêle en route"
        self._attr_device_class = "heat"


    @property
    def is_on(self):
        return self.tracker.binary_state

    @property
    def icon(self):
        if self.is_on:
            return "mdi:fire"          # ON → flamme
        return "mdi:fire-off"          # OFF → flamme éteinte

    


