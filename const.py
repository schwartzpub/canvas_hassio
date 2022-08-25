"""Constants for the canvas integration."""

from datetime import timedelta

NAME = "Canvas"
DOMAIN = "canvas"
VERSION = "0.0.1"

HA_SENSOR = ["sensor"]

SCAN_INTERVAL = timedelta(minutes=1)

CONF_BASEURI = "baseuri"
CONF_SECRET = "token"

STUDENTS = "Student(s)"
COURSES = "Course(s)"
ASSIGNMENTS = "Assignment(s)"

ATTR_STUDENTS = "_students"
ATTR_COURSES = "_courses"
ATTR_ASSIGNMENTS = "_assignments"