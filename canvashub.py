"""Canvas Hub."""
from __future__ import annotations

import logging

from canvas_parent_api import Canvas
from canvas_parent_api.models.course import Course
from canvas_parent_api.models.assignment import Assignment
from canvas_parent_api.models.observee import Observee

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_BASEURI, CONF_SECRET, DOMAIN, SCAN_INT

_LOGGER = logging.getLogger(__name__)

class CanvasHub(DataUpdateCoordinator):
    """Canvas Hub definition."""

    config_entry: config_entries.ConfigEntry

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INT)

        self._baseuri = self.config_entry.data[CONF_BASEURI]
        self._secret = self.config_entry.data[CONF_SECRET]

    async def poll_observees(self) -> list[Observee]:
        """Get Canvas Observees (students)."""
        client = Canvas(f"{self._baseuri}",f"{self._secret}")
        return await client.observees()

    async def poll_courses(self) -> list[Course]:
        """Get Canvas Courses."""
        courses: list[Course] = []

        client = Canvas(f"{self._baseuri}",f"{self._secret}")
        observees = await client.observees()
        for observee in observees:
            courseresp = await client.courses(observee.id)
            courses.extend([Course(course) for course in courseresp])
        return courses

    async def poll_assignments(self) -> list[Assignment]:
        """Get Canvas Assignments."""
        assignments: list[Assignment] = []

        client = Canvas(f"{self._baseuri}",f"{self._secret}")
        courses = await self.poll_courses()
        for course in courses:
            observee = course.enrollments[0]
            assignmentresp = await client.assignments(observee.get('user_id', ''),course.id)
            assignments.extend([Assignment(assignment) for assignment in assignmentresp])
        return assignments
