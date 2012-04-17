# -*- coding: utf-8 -*-
'''
Created on 15.04.2012

@author: moschlar
'''
#TODO: Unified field_order regarding common elements

import logging

from tg import expose, tmpl_context as c
from tg.decorators import paginate, with_trailing_slash
from tgext.crud import CrudRestController, EasyCrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller, FillerBase, EditFormFiller

from sauce.model import DBSession, Event, Lesson, Team, Student, Sheet, Assignment, Test, Teacher
from sprox.formbase import AddRecordForm, EditableForm

from tw.forms import TextField, BooleanRadioButtonList, SingleSelectField, FileField
from tw.forms.validators import Email, FieldsMatch, Schema
from tw.tinymce import TinyMCE
from formencode.validators import FieldStorageUploadConverter

log = logging.getLogger(__name__)

#--------------------------------------------------------------------------------

passwordValidator = Schema(chained_validators=(FieldsMatch('password',
                                                           '_password',
                                                            messages={'invalidNoMatch':
                                                                 "Passwords do not match"}),))

#--------------------------------------------------------------------------------

class FilteredCrudRestController(EasyCrudRestController):
    '''Generic base class for CrudRestControllers with filters'''
    
    # Merely a reminder of possible options
    __table_options__ = {
        '__omit_fields__':[],
        '__field_order__':[],
        }
    __form_options__ = {
        '__hide_fields__':[],
        '__field_order__':[],
        '__field_widget_types__':{},
        '__field_widget_args__':{},
        }
    
    def __init__(self, model=None, filters=[], filter_bys={}, 
                 table_options={}, form_options={}, menu_items={}):
        '''Initialize FilteredCrudRestController with given options
        
        Although not required, model should be given.
        table_options and form_options are merged into the defaults
        '''
        
        if model:
            self.model = model
        
        super(FilteredCrudRestController, self).__init__(DBSession, menu_items)
        
        def custom_do_get_provider_count_and_objs(**kw):
            '''Custom getter function respecting provided filters and filter_bys'''
            qry = model.query
            if filters:
                qry = qry.filter(*filters)
            if filter_bys:
                qry = qry.filter_by(**filter_bys)
            objs = qry.all()
            return len(objs), objs
        # Assign custom getter function to table_filler
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

#--------------------------------------------------------------------------------

class TeamsCrudController(FilteredCrudRestController):
    
    model = Team
    
    __table_options__ = {
        '__omit_fields__':['lesson_id'],
        '__field_order__':['id', 'name', 'lesson', 'students'],
        }
    __form_options__ = {
        '__omit_fields__':[],
        '__field_order__':['id', 'name', 'lesson', 'students'],
        '__field_widget_types__':{'name':TextField},
        }
    
class StudentsCrudController(FilteredCrudRestController):
    
    model = Student
    
    __table_options__ = {
        '__omit_fields__':['id', 'password', '_password', 'submissions', 'type', 'groups'],
        '__field_order__':['id', 'user_name', 'display_name', 'email_address', 'teams', 'created'],
        }
    __form_options__ = {
        '__omit_fields__':['submissions', 'type', 'created'],
        '__field_order__':['id', 'user_name', 'display_name', 'email_address', 'teams', 'password', '_password', 'groups'],
        '__field_widget_types__':{'user_name':TextField, 'display_name':TextField, 'email_address':TextField},
        '__base_validator__':passwordValidator,
        }

class TeachersCrudController(FilteredCrudRestController):
    
    model = Teacher
    
    __table_options__ = {
        '__omit_fields__':['id', 'password', '_password', 'type', 'groups', 'judgements', 'assignments', 'tests', 'sheets', 'news', 'events'],
        '__field_order__':['id', 'user_name', 'display_name', 'email_address', 'lessons', 'created'],
        }
    __form_options__ = {
        '__omit_fields__':['submissions', 'type', 'created', 'judgements', 'judgements', 'assignments', 'tests', 'sheets', 'news', 'events'],
        '__field_order__':['id', 'user_name', 'display_name', 'email_address', 'lessons', 'password', '_password', 'groups'],
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
        '__field_order__':['id', 'lesson_id', 'name', 'teacher', 'teams'],
        '__field_widget_types__':{'name':TextField},
        }

class SheetsCrudController(FilteredCrudRestController):
    
    model = Sheet
    
    __table_options__ = {
        '__omit_fields__':['id', 'description', 'event_id', 'event', 'teacher_id', '_url'],
        '__field_order__':['sheet_id', 'name', '_start_time', '_end_time', 
                           'public', 'teacher'],
        }
    __form_options__ = {
        '__hide_fields__':['_url'], 
        '__field_order__':['id', 'sheet_id', 'name', 'description', 
                           '_start_time', '_end_time', 'public', 'teacher'],
        '__field_widget_types__':{'name':TextField, 'description':TinyMCE, 'public':BooleanRadioButtonList},
        '__field_widget_args__':{'_start_time':{'default': u'', 'help_text': u'Leave empty to use value from event'},
                                 '_end_time':{'default': u'', 'help_text': u'Leave empty to use value from event'},}
        }

class AssignmentsCrudController(FilteredCrudRestController):
    
    model = Assignment
    
    __table_options__ = {
        '__omit_fields__':['id', 'event_id', '_event', 'teacher_id', 'teacher', '_teacher',
                           'sheet_id', 'description', 'tests', 'submissions', 'show_compiler_msg'],
        '__field_order__':['assignment_id', 'name', 'sheet', 
                           '_start_time', '_end_time', 'timeout', 
                           'allowed_languages', 'public'],
        }
    __form_options__ = {
        '__hide_fields__':['tests', 'submissions', '_event'], 
        '__field_order__':['id', 'assignment_id', 'sheet', 'name', 'description', 
                           '_start_time', '_end_time', 'timeout', 'allowed_languages',
                           'show_compiler_msg', 'tests', 'public', 'teacher'],
        '__field_widget_types__':{'name':TextField, 'description':TinyMCE, 
                                  'show_compiler_msg':BooleanRadioButtonList,
                                  'public': BooleanRadioButtonList},
        '__field_widget_args__':{'_start_time':{'default': u'', 'help_text': u'Leave empty to use value from sheet'},
                                 '_end_time':{'default': u'', 'help_text': u'Leave empty to use value from sheet'},}
        }

class TestsCrudController(FilteredCrudRestController):
    
    model = Test
    
    __table_options__ = {
        '__omit_fields__':['id', 'assignment_id', 'input_data', 'output_data', 'separator',
                           'ignore_case', 'ignore_returncode', 'show_partial_match',
                           'splitlines', 'split',
                           'parse_int', 'parse_float', 'sort',
                           'teacher_id', 'teacher', 'testruns'],
        '__field_order__':['assignment', 'visible', 'argv'],
        }
    __form_options__ = {
        '__hide_fields__':['testruns'],
        '__field_order__':['id', 'assignment', 'visible', '_timeout', 'argv',
                           'input_type', 'output_type', 'input_filename', 'output_filename',
                           'input_data', 'output_data', 'separator',
                           'ignore_case', 'ignore_returncode', 'show_partial_match', 'splitlines', 'split',
                           'parse_int', 'parse_float', 'sort',
                          ],
        '__field_widget_types__':{'argv': TextField,
                                  'visible': BooleanRadioButtonList,
                                  'input_filename': TextField, 'output_filename': TextField,
                                  'input_type': SingleSelectField, 'output_type': SingleSelectField,
                                  'input_data': FileField, 'output_data': FileField,
                                  #'separator':         BooleanRadioButtonList,
                                  'ignore_case':        BooleanRadioButtonList,
                                  'ignore_returncode':  BooleanRadioButtonList,
                                  'show_partial_match': BooleanRadioButtonList,
                                  'splitlines':         BooleanRadioButtonList,
                                  'split':              BooleanRadioButtonList,
                                  'parse_int':          BooleanRadioButtonList,
                                  'parse_float':        BooleanRadioButtonList,
                                  'sort':               BooleanRadioButtonList,
                                 },
        '__field_widget_args__':{'input_type':  dict(options=[('stdin','stdin'), ('file','file')]),
                                 'output_type': dict(options=[('stdout','stdout'), ('file','file')]),
                                 'input_data':  dict(help_text=u'Warning, this field always overwrites database entries.'),
                                 'output_data': dict(help_text=u'Warning, this field always overwrites database entries.'),
                                },
        '__field_validator_types__':{'input_data': FieldStorageUploadConverter,
                                     'output_data': FieldStorageUploadConverter,
                                    },
        }

class EventsCrudController(FilteredCrudRestController):
    #TODO: Wrong field_order in form
    
    model = Event
    
    __table_options__ = {
        '__omit_fields__':['id', 'description', 'teacher_id', 'password',
                           'assignments', 'lessons', 'sheets', 'news',
                           ],
        '__field_order__':['type', '_url', 'name', 'teacher', 'public',
                           'start_time', 'end_time', 'teachers'],
        }
    __form_options__ = {
        '__hide_fields__':['assignments', 'sheets', 'news'], 
        '__field_order__':['type', '_url', 'name', 'description' 'teacher', 'public',
                           'password', 'start_time', 'end_time', 'teachers'],
        '__field_widget_types__':{'name':TextField, 'description':TinyMCE, 
                                  'public': BooleanRadioButtonList, '_url':TextField,
                                  'type': SingleSelectField, 'password':TextField, 
                                  },
        '__field_widget_args__':{
                                'type': dict(options=[('course','Course'), ('contest','Contest')]),
                                }
        }

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    