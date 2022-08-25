"""The canvas integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

import logging
from .canvashub import CanvasHub
from .const import (
    CONF_BASEURI,
    CONF_SECRET,
    HA_SENSOR,
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

def setup (hass, config):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up canvas from a config entry."""

    hass.data.setdefault(DOMAIN,{})
    hass.data[DOMAIN][entry.entry_id] = CanvasHub(hass)

    _LOGGER.warning("-------SETTING UP PLATFORMS--------")
    
    hass.config_entries.async_setup_platforms(entry, HA_SENSOR)
        
    _LOGGER.warning("-------COMPLETED SETTING UP PLATFORMS---------")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, HA_SENSOR):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok