from __future__ import annotations

import logging
import aiohttp

from typing import Any, Dict
from datetime import datetime, date

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_BASEURI,
    CONF_SECRET,
    DOMAIN,
    SCAN_INTERVAL
)

_LOGGER = logging.getLogger(__name__)

class CanvasHub(DataUpdateCoordinator[Dict[str, Any]]):
    def __init__(
        self,
        hass: HomeAssistant
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

        self._baseuri = self.config_entry.data[CONF_BASEURI]
        self._secret = self.config_entry.data[CONF_SECRET]