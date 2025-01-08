"""Canvas Hub."""
from __future__ import annotations

import logging
import asyncio
import itertools

from canvas_parent_api import Canvas
from canvas_parent_api.models.assignment import Assignment
from canvas_parent_api.models.course import Course
from canvas_parent_api.models.observee import Observee
from canvas_parent_api.models.submission import Submission

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_BASEURI, CONF_SECRET, DEFAULT_SEMAPHORE, DOMAIN, SCAN_INT, CONF_SEMAPHORE

_LOGGER = logging.getLogger(__name__)


class CanvasHub(DataUpdateCoordinator):
    """Canvas Hub definition."""

    config_entry: config_entries.ConfigEntry

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INT)

        self._baseuri = self.config_entry.data[CONF_BASEURI]
        self._secret = self.config_entry.data[CONF_SECRET]
        self._client = Canvas(f"{self._baseuri}",f"{self._secret}")
        self._semaphore = asyncio.Semaphore(self.config_entry.options.get(CONF_SEMAPHORE, DEFAULT_SEMAPHORE))

    async def get_students(self):
        """Get handler for students."""
        return await self._client.observees()

    async def get_courses(self, student_id, sem):
        """Get handler for courses."""
        async with sem:
            return await self._client.courses(student_id)

    async def get_assignments(self, student_id, course_id, sem):
        """Get handler for assignments."""
        async with sem:
            return await self._client.assignments(student_id,course_id)

    async def get_submissions(self, student_id, course_id, sem):
        """Get handler for submissions."""
        async with sem:
            return await self._client.submissions(student_id,course_id)

    async def poll_observees(self) -> list[Observee]:
        """Get Canvas Observees (students)."""
        return await self.get_students()

    async def poll_courses(self) -> list[Course]:
        """Get Canvas Courses."""
        courses: list[Course] = []

        observees = await self.get_students()
        for observee in observees:
            courseresp = await self.get_courses(observee.id, self._semaphore)
            #courses.extend([Course(course) for course in courseresp])
        return courseresp

    async def poll_assignments(self) -> list[Assignment]:
        """Get Canvas Assignments."""
        assignments: list[Assignment] = []
        assignment_tasks = []

        courses = await self.poll_courses()
        for course in courses:
            observee = course.enrollments[0]
            if observee is not None:
                assignment_tasks.append(asyncio.create_task(self.get_assignments(observee['user_id'], course.id, self._semaphore)))
        assignment_results = await asyncio.gather(*assignment_tasks)
        #assignments.extend([Assignment(assignment) for assignment in itertools.chain.from_iterable(assignment_results)])
        return assignment_results

    async def poll_submissions(self) -> list[Submission]:
        """Get Canvas Assignments."""
        submissions: list[Submission] = []
        submission_tasks = []

        courses = await self.poll_courses()
        for course in courses:
            observee = course.enrollments[0]
            if observee is not None:
                submission_tasks.append(asyncio.create_task(self.get_submissions(observee['user_id'], course.id, self._semaphore)))
        submission_results = await asyncio.gather(*submission_tasks)
        #submissions.extend( [Submission(submission) for submission in itertools.chain.from_iterable(submission_results)])
        return submission_results
