"""Constants for the canvas integration."""

from datetime import timedelta

NAME = "Canvas"
DOMAIN = "canvas"
VERSION = 1

HA_SENSOR = ["sensor"]

SCAN_INT = timedelta(minutes=10)

CONF_BASEURI = "baseuri"
CONF_SECRET = "token"
CONF_SEMAPHORE = "semaphore"
DEFAULT_SEMAPHORE = 15

STUDENTS = "Student(s)"
COURSES = "Course(s)"
ASSIGNMENTS = "Assignment(s)"

ATTR_STUDENTS = "_students"
ATTR_COURSES = "_courses"
ATTR_ASSIGNMENTS = "_assignments"
