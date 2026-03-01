""" Le Config Flow """

import logging

from homeassistant.config_entries import ConfigFlow
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class TutoHACSConfigFlow(ConfigFlow, domain=DOMAIN):
    """La classe qui implémente le config flow pour notre DOMAIN.
    Elle doit dériver de FlowHandler"""

    # La version de notre configFlow. Va permettre de migrer les entités
    # vers une version plus récente en cas de changement
    VERSION = 1
