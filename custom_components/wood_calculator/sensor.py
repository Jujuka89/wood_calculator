from datetime import datetime, timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity

from .const import *


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    temp_sensor = config.get("poele_sensor")
    seuil = config.get("temp_seuil", DEFAULT_TEMP_SEUIL)
    duree_buche = config.get("duree_buche", DEFAULT_DUREE_BUCHE)
    buches_stere = config.get("buches_stere", DEFAULT_BUCHES_STERE)
    prix_stere = config.get("prix_stere", DEFAULT_PRIX_STERE)
    debut_chauffe_mois = config.get("debut_chauffe_mois", DEFAULT_DEBUT_CHAUFFE_MOIS)

    tracker = WoodTracker(hass, temp_sensor, seuil, duree_buche, debut_chauffe_mois)

    entities = [
        WoodLogsSensor(tracker),
        WoodStereSensor(tracker, buches_stere),
        WoodSeasonStereSensor(tracker, buches_stere),
        WoodCostSensor(tracker, buches_stere, prix_stere),
        WoodBinarySensor(tracker),
    ]
    async_add_entities(entities)
    tracker.start()


class WoodTracker:
    """Compteur de temps de fonctionnement du poêle."""

    def __init__(self, hass, temp_sensor, seuil, duree_buche, debut_chauffe_mois):
        self.hass = hass
        self.temp_sensor = temp_sensor
        self.seuil = seuil
        self.duree_buche = duree_buche
        self.debut_chauffe_mois = min(12, max(1, int(debut_chauffe_mois)))

        now = datetime.now()
        self.minutes_on = 0
        self.season_minutes_on = 0
        self.last_day = now.day
        self.current_season = self._season_label(now)
        self._binary_state = False

    def _season_start_year(self, value_date):
        if value_date.month >= self.debut_chauffe_mois:
            return value_date.year
        return value_date.year - 1

    def _season_label(self, value_date):
        season_start = self._season_start_year(value_date)
        return f"{season_start}-{season_start + 1}"

    def start(self):
        async_track_time_interval(self.hass, self.update, timedelta(minutes=1))

    async def update(self, now):
        # `now` est fourni par Home Assistant à chaque tick minute.
        current_time = now if isinstance(now, datetime) else datetime.now()

        if current_time.day != self.last_day:
            self.minutes_on = 0
            self.last_day = current_time.day

        new_season = self._season_label(current_time)
        if new_season != self.current_season:
            self.season_minutes_on = 0
            self.current_season = new_season

        state = self.hass.states.get(self.temp_sensor)
        if not state or state.state in ("unknown", "unavailable"):
            self._binary_state = False
            return

        try:
            temp = float(state.state)
        except ValueError:
            self._binary_state = False
            return

        if temp >= self.seuil:
            self.minutes_on += 1
            self.season_minutes_on += 1
            self._binary_state = True
        else:
            self._binary_state = False

    def restore_season_stere(self, season_stere, buches_stere, restored_season):
        if restored_season == self.current_season:
            logs = season_stere * buches_stere
            self.season_minutes_on = round(logs * self.duree_buche)

    @property
    def logs(self):
        return round(self.minutes_on / self.duree_buche, 2)

    @property
    def season_logs(self):
        return round(self.season_minutes_on / self.duree_buche, 2)

    @property
    def binary_state(self):
        return self._binary_state


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


class WoodSeasonStereSensor(SensorEntity, RestoreEntity):
    def __init__(self, tracker, buches_stere):
        self.tracker = tracker
        self.buches_stere = buches_stere
        self._attr_name = "Consommation Bois (stère saison)"
        self._attr_native_unit_of_measurement = "st"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        last_state = await self.async_get_last_state()

        if not last_state or last_state.state in ("unknown", "unavailable"):
            return

        try:
            restored_stere = float(last_state.state)
        except ValueError:
            return

        restored_season = last_state.attributes.get("periode_chauffe", self.tracker.current_season)
        self.tracker.restore_season_stere(restored_stere, self.buches_stere, restored_season)

    @property
    def native_value(self):
        return round(self.tracker.season_logs / self.buches_stere, 4)

    @property
    def extra_state_attributes(self):
        return {
            "periode_chauffe": self.tracker.current_season,
            "debut_chauffe_mois": self.tracker.debut_chauffe_mois,
        }


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
    """Binary sensor pour poêle en route."""

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
            return "mdi:fire"
        return "mdi:fire-off"
