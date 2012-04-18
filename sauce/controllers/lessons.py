# -*- coding: utf-8 -*-
"""Lessons controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, abort, request
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.model import Lesson, Team, Student, Event
from sauce.controllers.crc import FilteredCrudRestController, TeamsCrudController, StudentsCrudController, LessonsCrudController
from sauce.lib.auth import has_teachers
from repoze.what.predicates import Any, has_permission

log = logging.getLogger(__name__)


class LessonsController(LessonsCrudController):
    
    model = Lesson
    
    def __init__(self, event, **kw):
        self.event = event
        super(LessonsController, self).__init__(model=Lesson, inject=dict(teacher=request.teacher), filter_bys=dict(event_id=self.event.id), 
                                                menu_items={'lesson': Lesson, 'lessons/team': Team, 'lessons/student': Student}, **kw)
        
        self.teams = TeamsCrudController(model=Team, filters=[Team.lesson_id.in_((l.id for l in self.event.lessons))], 
                                     menu_items={'../lesson': Lesson, '../lessons/team': Team, '../lessons/student': Student}, **kw)
        self.students = StudentsCrudController(model=Student, filters=[Student.id.in_((s.id for l in self.event.lessons for t in l.teams for s in t.students))], 
                                           menu_items={'../lesson': Lesson, '../lessons/team': Team, '../lessons/student': Student}, **kw)
        
        self.allow_only = Any(has_teachers(Event, self.event.id), has_permission('manage'))


