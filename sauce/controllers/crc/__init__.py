# -*- coding: utf-8 -*-
"""CrudRestControllers for the SAUCE application.

@see: :mod:`tgext.crud`
@see: :mod:`sprox`
"""
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from sauce.controllers.crc.base import FilterCrudRestController
from sauce.controllers.crc.assignment import SheetsCrudController, AssignmentsCrudController
from sauce.controllers.crc.event import EventsCrudController, LessonsCrudController
from sauce.controllers.crc.news import NewsItemController
from sauce.controllers.crc.test import TestsCrudController
from sauce.controllers.crc.user import TeamsCrudController, StudentsCrudController, TutorsCrudController

__all__ = [
    'TeamsCrudController',
    'StudentsCrudController',
    'TutorsCrudController',
    'EventsCrudController',
    'LessonsCrudController',
    'SheetsCrudController',
    'AssignmentsCrudController',
    'TestsCrudController',
    'NewsItemController',
]
