# -*- coding: utf-8 -*-
"""Lessons controller module

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
from sauce.model import DBSession, Lesson, Team, Student
from sauce.controllers.crc import FilteredCrudRestController

from tw.forms import TextField

log = logging.getLogger(__name__)


class TeamsController(FilteredCrudRestController):
    
    model = Team
    
    __table_options__ = {
        '__omit_fields__':['lesson_id'],
        '__field_order__':['id', 'name', 'lesson', 'students'],
        }
    __form_options__ = {
        '__field_widget_types__':{'name':TextField},
        }
    
    def __init__(self, event, session):
        super(TeamsController, self).__init__(model=Team, filters=[Team.lesson_id.in_((l.id for l in event.lessons))], session=session)
        self.menu_items = {'../lesson': Lesson, '../lessons/team': Team, '../lessons/student': Student}
    
class StudentsController(FilteredCrudRestController):
    
    model = Student
    
    __table_options__ = {
        '__omit_fields__':['id', 'password', '_password', 'submissions', 'type', 'groups'],
        '__field_order__':['id', 'user_name', 'display_name', 'email_address', 'teams', 'created'],
        }
    __form_options__ = {
        '__omit_fields__':['id', 'submissions', 'type', 'created'],
        '__field_order__':['id', 'user_name', 'display_name', 'email_address', 'teams', 'password', '_password', 'groups'],
        '__field_widget_types__':{'user_name':TextField, 'display_name':TextField, 'email_address':TextField},
        }
    def __init__(self, event, session):
        super(StudentsController, self).__init__(model=Student, filters=[Student.id.in_((s.id for l in event.lessons for t in l.teams for s in t.students))], session=session)
        self.menu_items = {'../lesson': Lesson, '../lessons/team': Team, '../lessons/student': Student}

class LessonsController(FilteredCrudRestController):
    
    model = Lesson
    
    __table_options__ = {
        '__omit_fields__':['id', 'event_id', 'event', 'teacher_id'],
        '__field_order__':['lesson_id', 'name', 'teacher', 'teams'],
        }
    __form_options__ = {
#        '__hide_fields__':['event', 'teacher'], # If we hide them, creation of new lessons is not possible
        '__field_order__':['lesson_id', 'name', 'teacher', 'teams'],
        '__field_widget_types__':{'name':TextField},
        }
        
    def __init__(self, event, session):
        self.event = event
        super(LessonsController, self).__init__(model=Lesson, session=session, filter_bys=dict(event_id=event.id))
        self.teams = TeamsController(event=event, session=DBSession)
        self.students = StudentsController(event=event, session=DBSession)
        self.menu_items = {'lesson': Lesson, 'lessons/team': Team, 'lessons/student': Student}
    

