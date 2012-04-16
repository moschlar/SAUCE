# -*- coding: utf-8 -*-
"""EventAdmin controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, abort
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.model import Lesson, Team, Student, Sheet, Assignment, Test, Event
from sauce.controllers.crc import FilteredCrudRestController, TeamsCrudController, StudentsCrudController, LessonsCrudController, SheetsCrudController, AssignmentsCrudController,\
    TestsCrudController, EventsCrudController
from sauce.lib.base import BaseController

log = logging.getLogger(__name__)


class EventAdminController(BaseController):
    
    def __init__(self, event, **kw):
        
        self.event = event
        
        model_items = [Event, Lesson, Student, Team, Sheet, Assignment, Test]
        menu_items = dict([(m.__name__.lower(), m) for m in model_items])
        
        self.events = EventsCrudController(model=Event, filter_bys=dict(id=self.event.id),
                                           menu_items=menu_items, **kw)
        
        self.lessons = LessonsCrudController(model=Lesson, filter_bys=dict(event_id=self.event.id),
                                             menu_items=menu_items, **kw)
        
        self.teams = TeamsCrudController(model=Team, filters=[Team.lesson_id.in_((l.id for l in self.event.lessons))], 
                                     menu_items=menu_items, **kw)
        
        self.students = StudentsCrudController(model=Student, filters=[Student.id.in_((s.id for l in self.event.lessons for t in l.teams for s in t.students))], 
                                           menu_items=menu_items, **kw)
        
        self.sheets = SheetsCrudController(model=Sheet, filter_bys=dict(event_id=self.event.id),
                                           menu_items=menu_items, **kw)
        
        self.assignments = AssignmentsCrudController(model=Assignment, filters=[Assignment.sheet_id.in_((s.id for s in self.event.sheets))], 
                                     menu_items=menu_items, **kw)
        
        self.tests = TestsCrudController(model=Test, filters=[Test.assignment_id.in_((a.id for s in self.event.sheets for a in s.assignments))],
                                         menu_items=menu_items, **kw)
        
    @expose('mako:sauce.templates.admin_index')
    def index(self):
        return dict()

