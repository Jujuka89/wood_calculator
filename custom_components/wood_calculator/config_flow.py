"""Config flow for Wood Calculator."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import (
    DEFAULT_BUCHES_STERE,
    DEFAULT_DEBUT_CHAUFFE_MOIS,
    DEFAULT_DUREE_BUCHE,
    DEFAULT_PRIX_STERE,
    DEFAULT_TEMP_SEUIL,
    DOMAIN,
)


class WoodCalculatorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wood Calculator."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(user_input["poele_sensor"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Wood Calculator",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required("poele_sensor"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required("temp_seuil", default=DEFAULT_TEMP_SEUIL): vol.Coerce(float),
                vol.Required("duree_buche", default=DEFAULT_DUREE_BUCHE): vol.Coerce(float),
                vol.Required("buches_stere", default=DEFAULT_BUCHES_STERE): vol.Coerce(float),
                vol.Required("prix_stere", default=DEFAULT_PRIX_STERE): vol.Coerce(float),
                vol.Required(
                    "debut_chauffe_mois", default=DEFAULT_DEBUT_CHAUFFE_MOIS
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=12)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
