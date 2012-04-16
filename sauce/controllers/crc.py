# -*- coding: utf-8 -*-
'''
Created on 15.04.2012

@author: moschlar
'''

import logging

from tg import expose, tmpl_context as c
from tg.decorators import paginate, with_trailing_slash
from tgext.crud import CrudRestController, EasyCrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller, FillerBase, EditFormFiller

from sauce.model import DBSession, Event, Lesson, Team, Student
from sprox.formbase import AddRecordForm, EditableForm

from tw.forms import TextField
from tw.forms.validators import Email, FieldsMatch, Schema

log = logging.getLogger(__name__)


#--------------------------------------------------------------------------------

class FilteredCrudRestController(EasyCrudRestController):
    '''Generic base class for CrudRestControllers with filters'''
    
    __table_options__ = {
        '__omit_fields__':[],
        '__field_order__':[],
        }
    __form_options__ = {
        '__hide_fields__':[],
        '__field_order__':[],
        '__field_widget_types__':{},
        }
    
    def __init__(self, model=None, filters=[], filter_bys={}, 
                 table_options={}, form_options={}, menu_items={}):
        
        if model:
            self.model = model
        
        super(FilteredCrudRestController, self).__init__(DBSession)
        
        # Custom getter function respecting provided filters
        def custom_do_get_provider_count_and_objs(**kw):
            qry = model.query
            if filters:
                qry = qry.filter(*filters)
            if filter_bys:
                qry = qry.filter_by(**filter_bys)
            objs = qry.all()
            return len(objs), objs
        
        self.table_filler._do_get_provider_count_and_objs = custom_do_get_provider_count_and_objs
        
        # Update table options
        for opt in table_options:
            if self.__table_options__.get(opt):
                self.__table_options__[opt].update(table_options[opt])
            else:
                self.__table_options__[opt] = table_options[opt]
        # Update form options
        for opt in form_options:
            if self.__form_options__.get(opt):
                self.__form_options__[opt].update(form_options[opt])
            else:
                self.__form_options__[opt] = form_options[opt]
        
        # Update menu items
        if menu_items:
            self.menu_items = menu_items

#--------------------------------------------------------------------------------

passwordValidator = Schema(chained_validators=(FieldsMatch('password',
                                                           '_password',
                                                            messages={'invalidNoMatch':
                                                                 "Passwords do not match"}),))

class TeamsCrudController(FilteredCrudRestController):
    
    model = Team
    
    __table_options__ = {
        '__omit_fields__':['lesson_id'],
        '__field_order__':['id', 'name', 'lesson', 'students'],
        }
    __form_options__ = {
        '__field_widget_types__':{'name':TextField},
        }
    
class StudentsCrudController(FilteredCrudRestController):
    
    model = Student
    
    __table_options__ = {
        '__omit_fields__':['id', 'password', '_password', 'submissions', 'type', 'groups'],
        '__field_order__':['id', 'user_name', 'display_name', 'email_address', 'teams', 'created'],
        }
    __form_options__ = {
        '__omit_fields__':['id', 'submissions', 'type', 'created'],
        '__field_order__':['id', 'user_name', 'display_name', 'email_address', 'teams', 'password', '_password', 'groups'],
        '__field_widget_types__':{'user_name':TextField, 'display_name':TextField, 'email_address':TextField},
        '__base_validator__':passwordValidator,
        }

class LessonsCrudController(FilteredCrudRestController):
    
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

#--------------------------------------------------------------------------------


