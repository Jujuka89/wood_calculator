from datetime import timedelta, datetime
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from .const import *

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensor_temp = config.get("poele_sensor")
    seuil = config.get("temp_seuil", DEFAULT_TEMP_SEUIL)
    duree_buche = config.get("duree_buche", DEFAULT_DUREE_BUCHE)
    buches_stere = config.get("buches_stere", DEFAULT_BUCHES_STERE)
    prix_stere = config.get("prix_stere", DEFAULT_PRIX_STERE)

    tracker = WoodTracker(hass, sensor_temp, seuil, duree_buche)

    async_add_entities([
        WoodLogsSensor(tracker),
        WoodStereSensor(tracker, buches_stere),
        WoodCostSensor(tracker, buches_stere, prix_stere)
    ])

    tracker.start()


class WoodTracker:
    def __init__(self, hass, sensor_temp, seuil, duree_buche):
        self.hass = hass
        self.sensor_temp = sensor_temp
        self.seuil = seuil
        self.duree_buche = duree_buche
        self.minutes_on = 0
        self.last_day = datetime.now().day

    def start(self):
        async_track_time_interval(
            self.hass,
            self.update,
            timedelta(minutes=1)
        )

    async def update(self, now):
        today = datetime.now().day

        # Reset automatique à minuit
        if today != self.last_day:
            self.minutes_on = 0
            self.last_day = today

        state = self.hass.states.get(self.sensor_temp)

        if state and state.state not in ("unknown", "unavailable"):
            if float(state.state) >= self.seuil:
                self.minutes_on += 1

    @property
    def logs(self):
        return round(self.minutes_on / self.duree_buche, 2)


class WoodLogsSensor(SensorEntity):
    def __init__(self, tracker):
        self.tracker = tracker
        self._attr_name = "Logs Burned (Day)"
        self._attr_native_unit_of_measurement = "logs"

    @property
    def native_value(self):
        return self.tracker.logs


class WoodStereSensor(SensorEntity):
    def __init__(self, tracker, buches_stere):
        self.tracker = tracker
        self.buches_stere = buches_stere
        self._attr_name = "Wood Consumption (Stere)"
        self._attr_native_unit_of_measurement = "st"

    @property
    def native_value(self):
        return round(self.tracker.logs / self.buches_stere, 4)


class WoodCostSensor(SensorEntity):
    def __init__(self, tracker, buches_stere, prix_stere):
        self.tracker = tracker
        self.buches_stere = buches_stere
        self.prix_stere = prix_stere
        self._attr_name = "Wood Cost (Day)"
        self._attr_native_unit_of_measurement = "€"

    @property
    def native_value(self):
        stere = self.tracker.logs / self.buches_stere
        return round(stere * self.prix_stere, 2)

