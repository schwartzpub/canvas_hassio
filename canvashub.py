"""Canvas Hub."""
from __future__ import annotations

import logging
import aiohttp

from datetime import datetime
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

    async def poll_observees(self) -> list:
        """Get Canvas Observees (students)."""
        async with aiohttp.ClientSession() as session:
            async with session.get('{0}/api/v1/users/self/observees'.format('https://rsdmo.instructure.com'),headers={'Accept': 'application/json', 'Authorization': 'Bearer {0}'.format(self._secret)}) as studentresp:
                resp = await studentresp.json()
                return resp

    async def poll_courses(self) -> list:
        """Get Canvas Courses."""
        courses = []
        observees = await self.poll_observees()
        today = datetime.now()
        for observee in observees:
            async with aiohttp.ClientSession() as session:
                async with session.get('{0}/api/v1/users/{1}/courses?include[]=term'.format('https://rsdmo.instructure.com',observee['id']),headers={'Accept': 'application/json', 'Authorization': 'Bearer {0}'.format(self._secret)}) as courseresp:
                    resp = await courseresp.json()
                    for course in resp:
                        if course["term"] != None:
                            if datetime.strptime(course["term"]["start_at"],'%Y-%m-%dT%H:%M:%SZ') < today < datetime.strptime(course["term"]["end_at"],'%Y-%m-%dT%H:%M:%SZ'):
                                courses.append(course)
        return courses

    async def poll_assignments(self) -> list:
        """Get Canvas Assignments."""
        assignments = []
        courses = await self.poll_courses()
        for course in courses:
            observee = course['enrollments'][0]['user_id']
            async with aiohttp.ClientSession() as session:
                async with session.get('{0}/api/v1/users/{1}/courses/{2}/assignments?include[]=submission'.format('https://rsdmo.instructure.com',observee,course['id']),headers={'Accept': 'application/json', 'Authorization': 'Bearer {0}'.format(self._secret)}) as assignmentresp:
                    resp = await assignmentresp.json()
                    for assignment in resp:
                        assignments.append(assignment)
        return assignments