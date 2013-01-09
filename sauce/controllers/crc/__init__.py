# -*- coding: utf-8 -*-
"""CrudRestControllers for the SAUCE application."""

from sauce.controllers.crc.base import FilteredCrudRestController
from sauce.controllers.crc.assignment import SheetsCrudController, AssignmentsCrudController
from sauce.controllers.crc.event import EventsCrudController, LessonsCrudController
from sauce.controllers.crc.news import NewsItemController
from sauce.controllers.crc.test import TestsCrudController
from sauce.controllers.crc.user import TeamsCrudController, StudentsCrudController, TutorsCrudController

__all__ = ['TeamsCrudController', 'StudentsCrudController', 'TutorsCrudController',
    'EventsCrudController', 'LessonsCrudController',
    'SheetsCrudController', 'AssignmentsCrudController', 'TestsCrudController',
    'NewsItemController']
