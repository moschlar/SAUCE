# -*- coding: utf-8 -*-
"""EventAdmin controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, abort, request, tmpl_context as c
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.model import Lesson, Team, Student, Sheet, Assignment, Test, Event, Teacher
from sauce.controllers.crc import FilteredCrudRestController, TeamsCrudController, StudentsCrudController,\
    LessonsCrudController, SheetsCrudController, AssignmentsCrudController,\
    TestsCrudController, EventsCrudController, TeachersCrudController
from sauce.lib.base import BaseController
from sauce.lib.auth import has_teacher
from repoze.what.predicates import Any, has_permission
from tg.decorators import without_trailing_slash

log = logging.getLogger(__name__)



class EventAdminController(BaseController):
    ''''''
    
    
    def __init__(self, event, **kw):
        
        self.event = event
        
        model_items = [Event, Lesson, Student, Team, Sheet, Assignment, Test, Teacher]
        self.menu_items = dict([(m.__name__.lower(), m) for m in model_items])
        
        self.events = EventsCrudController(inject=dict(teacher=request.teacher),
                                           filter_bys=dict(id=self.event.id),
                                           menu_items=self.menu_items, **kw)
        
        self.lessons = LessonsCrudController(inject=dict(event=self.event),
                                             filter_bys=dict(event_id=self.event.id),
                                             menu_items=self.menu_items, **kw)
        
        self.teams = TeamsCrudController(filters=[Team.lesson_id.in_((l.id for l in self.event.lessons))],
                                         menu_items=self.menu_items, **kw)
        
        self.students = StudentsCrudController(#filters=[Student.id.in_((s.id for l in self.event.lessons for t in l.teams for s in t.students))],
                                               menu_items=self.menu_items, **kw)
        
        self.teachers = TeachersCrudController(#filters=[Teacher.id.in_((l.teacher.id for l in self.event.lessons))],
                                               menu_items=self.menu_items, **kw)
        
        
        self.sheets = SheetsCrudController(inject=dict(event=self.event, teacher=request.teacher),
                                           filter_bys=dict(event_id=self.event.id),
                                           menu_items=self.menu_items, **kw)
        
        self.assignments = AssignmentsCrudController(inject=dict(teacher=request.teacher),
                                                     filters=[Assignment.sheet_id.in_((s.id for s in self.event.sheets))],
                                                     menu_items=self.menu_items, **kw)
        
        self.tests = TestsCrudController(inject=dict(teacher=request.teacher),
                                         filters=[Test.assignment_id.in_((a.id for s in self.event.sheets for a in s.assignments))],
                                         menu_items=self.menu_items, **kw)
        
        self.allow_only = Any(has_teacher(Event, self.event.id), has_permission('manage'))
        
    
    @without_trailing_slash
    @expose('sauce.templates.event_admin')
    def index(self):
        return dict(page='events', event=self.event, menu_items=self.menu_items)

