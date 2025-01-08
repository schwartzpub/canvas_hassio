"""Platform for sensor integration."""
from __future__ import annotations

import logging
import json

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SCAN_INT

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = SCAN_INT

@dataclass
class CanvasEntityDescriptionMixin:
    """Mixin for required keys."""

    value_fn: Callable
    unique_id: str


@dataclass
class CanvasEntityDescription(
    SensorEntityDescription, CanvasEntityDescriptionMixin
):
    """Describes AdGuard Home sensor entity."""

SENSORS: tuple[CanvasEntityDescription, ...] = (
    CanvasEntityDescription(
        key="student",
        name="Canvas Students",
        unique_id="canvas_student",
        value_fn=lambda canvas: canvas.poll_observees()
    ),
    CanvasEntityDescription(
        key="course",
        name="Canvas Courses",
        unique_id="canvas_course",
        value_fn=lambda canvas: canvas.poll_courses()
    ),
    CanvasEntityDescription(
        key="assignment",
        name="Canvas Assignments",
        unique_id="canvas_assignment",
        value_fn=lambda canvas: canvas.poll_assignments()
    ),
    CanvasEntityDescription(
        key="submission",
        name="Canvas Submissions",
        unique_id="canvas_submission",
        value_fn=lambda canvas: canvas.poll_submissions()
    )
)

async def async_setup_entry(
    hass: HomeAssistant, 
    config_entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
    ):
    """Set up the sensor platform."""
    hub = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [CanvasSensor(description, hub) for description in SENSORS],
        True,
    )


class CanvasSensor(SensorEntity):
    """Canvas Sensor Definition."""
    entity_description: CanvasEntityDescription

    def __init__(
        self,
        description: CanvasEntityDescription,
        hub
    ) -> None:
        self._hub = hub
        self._attr_name = description.name
        self._attr_unique_id = f"{description.unique_id}"
        self._entity_description = description
        self._attr_canvas_data = {}    

    @property
    def extra_state_attributes(self):
        """Add extra attribute."""
        #return {f"{self._entity_description.key}": [x.as_dict() for x in self._attr_canvas_data]}
        return {f"{self._entity_description.key}": self._attr_canvas_data}
    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        canvasdata = await self._entity_description.value_fn(self._hub)
        self._attr_canvas_data = json.loads(json.dumps(canvasdata, default=lambda s: vars(s)))
        return
