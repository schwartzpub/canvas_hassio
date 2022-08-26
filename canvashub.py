"""Canvas Hub"""
from __future__ import annotations

import logging

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_BASEURI,
    CONF_SECRET,
    DOMAIN,
    SCAN_INT
)

_LOGGER = logging.getLogger(__name__)

class CanvasHub(DataUpdateCoordinator[dict[str, Any]]):
    """Canvas Hub definition"""
    def __init__(
        self,
        hass: HomeAssistant
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INT,
        )

        self._baseuri = self.config_entry.data[CONF_BASEURI]
        self._secret = self.config_entry.data[CONF_SECRET]