from datetime import timedelta, datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity
from .const import *

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    temp_sensor = config.get("poele_sensor")
    seuil = config.get("temp_seuil", DEFAULT_TEMP_SEUIL)
    duree_buche = config.get("duree_buche", DEFAULT_DUREE_BUCHE)
    buches_stere = config.get("buches_stere", DEFAULT_BUCHES_STERE)
    prix_stere = config.get("prix_stere", DEFAULT_PRIX_STERE)

    # Création tracker
    tracker = WoodTracker(hass, temp_sensor, seuil, duree_buche, buches_stere)

    # Capteurs
    log_sensor = WoodLogsSensor(tracker)
    stere_sensor = WoodStereSensor(tracker)
    stere_year_sensor = WoodStereYearSensor(tracker)
    stere_total_sensor = WoodStereTotalSensor(tracker)
    cost_sensor = WoodCostSensor(tracker, prix_stere)
    binary_sensor_poele = WoodBinarySensor(tracker)

    # Ajouter les entités
    async_add_entities([
        log_sensor,
        stere_sensor,
        cost_sensor,
        binary_sensor_poele,
        stere_year_sensor,
        stere_total_sensor
    ])

    # Démarrer le tracker
    tracker.start()


# ============================================================
# TRACKER
# ============================================================

class WoodTracker:
    """Tracker du poêle avec compteurs journalier, annuel et total"""
    def __init__(self, hass, temp_sensor, seuil, duree_buche, buches_stere):
        self.hass = hass
        self.temp_sensor = temp_sensor
        self.seuil = seuil
        self.duree_buche = duree_buche
        self.buches_stere = buches_stere

        self.minutes_on = 0
        self.last_day = datetime.now().day
        self.last_year = datetime.now().year

        self.stere_year = 0
        self.stere_total = 0
        self._binary_state = False

    def start(self):
        async_track_time_interval(
            self.hass,
            self.update,
            timedelta(minutes=1)
        )

    async def update(self, now):
        today = datetime.now().day
        current_year = datetime.now().year

        # Reset annuel le 1er janvier
        if current_year != self.last_year:
            self.stere_year = 0
            self.last_year = current_year

        # Reset quotidien + cumul annuel et total
        if today != self.last_day:
            if self.buches_stere:
                daily_stere = self.logs / self.buches_stere
                self.stere_year += daily_stere
                self.stere_total += daily_stere
            self.minutes_on = 0
            self.last_day = today

        # Mise à jour état poêle
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
    def stere_today(self):
        if self.buches_stere:
            return round(self.logs / self.buches_stere, 4)
        return 0

    @property
    def binary_state(self):
        return self._binary_state


# ============================================================
# CAPTEURS
# ============================================================

class WoodLogsSensor(SensorEntity):
    """Bûches brûlées par jour"""
    def __init__(self, tracker):
        self.tracker = tracker
        self._attr_name = "Bûches brûlées (jour)"
        self._attr_native_unit_of_measurement = "bûches"

    @property
    def native_value(self):
        return self.tracker.logs


class WoodStereSensor(SensorEntity):
    """Consommation bois journalier en stère"""
    def __init__(self, tracker):
        self.tracker = tracker
        self._attr_name = "Consommation Bois (stère)"
        self._attr_native_unit_of_measurement = "st"

    @property
    def native_value(self):
        return self.tracker.stere_today


class WoodStereYearSensor(SensorEntity, RestoreEntity):
    """Consommation bois annuel persistant"""
    def __init__(self, tracker):
        self.tracker = tracker
        self._attr_name = "Consommation Bois (année)"
        self._attr_native_unit_of_measurement = "st"
        self._attr_state_class = "total_increasing"

    async def async_added_to_hass(self):
        last_state = await self.async_get_last_state()
        if last_state:
            try:
                self.tracker.stere_year = float(last_state.state)
            except ValueError:
                self.tracker.stere_year = 0

    @property
    def native_value(self):
        return round(self.tracker.stere_year, 3)


class WoodStereTotalSensor(SensorEntity, RestoreEntity):
    """Consommation bois totale depuis toujours"""
    def __init__(self, tracker):
        self.tracker = tracker
        self._attr_name = "Consommation Bois (total)"
        self._attr_native_unit_of_measurement = "st"
        self._attr_state_class = "total_increasing"

    async def async_added_to_hass(self):
        last_state = await self.async_get_last_state()
        if last_state:
            try:
                self.tracker.stere_total = float(last_state.state)
            except ValueError:
                self.tracker.stere_total = 0

    @property
    def native_value(self):
        return round(self.tracker.stere_total, 3)


class WoodCostSensor(SensorEntity):
    """Coût journalier du bois"""
    def __init__(self, tracker, prix_stere):
        self.tracker = tracker
        self.prix_stere = prix_stere
        self._attr_name = "Coût Bois (jour)"
        self._attr_native_unit_of_measurement = "€"

    @property
    def native_value(self):
        return round(self.tracker.stere_today * self.prix_stere, 2)


class WoodBinarySensor(BinarySensorEntity):
    """Poêle en route"""
    def __init__(self, tracker):
        self.tracker = tracker
        self._attr_name = "Poêle en route"
        self._attr_device_class = "heat"

    @property
    def is_on(self):
        return self.tracker.binary_state

    @property
    def icon(self):
        return "mdi:fire" if self.is_on else "mdi:fire-off"
