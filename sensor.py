"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity
)

from homeassistant.core import HomeAssistant

from .const import (
    SCAN_INT,
    DOMAIN
)

import logging
_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = SCAN_INT

async def async_setup_entry(hass,config_entry,async_add_entities):
    """Set up the sensor platform."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [CanvasStudentSensor(hass,hub),CanvasCourseSensor(hass,hub)]
    )

class CanvasStudentSensor(SensorEntity):
    """Canvas Student entity definition""" 
    def __init__(
        self,
        hass: HomeAssistant,
        hub
    ) -> None:
        self._attr_name = "Canvas Students"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = None
        self._attr_unique_id = "canvas_student"
        self._hub = hub
        self._hass = hass
        self._attr_json = "test"

    @property
    def extra_state_attributes(self):
        return {
            "json": self._attr_json
        }

    async def async_update(self) -> str:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_json = "test"

class CanvasCourseSensor(SensorEntity):
    """Canvas Course entity definition"""
    def __init__(
        self,
        hass: HomeAssistant,
        hub
    ) -> None:
        self._attr_name = "Canvas Courses"
        self._attr_native_unit_of_measurement = None
        self._attr_device_class = None
        self._attr_state_class = None
        self._attr_unique_id = "canvas_course"
        self._hub = hub
        self._hass = hass
        self._attr_json = "test"

    @property
    def extra_state_attributes(self):
        return {
            "json": self._attr_json
        }

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_json = "test"