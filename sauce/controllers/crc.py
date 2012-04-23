# -*- coding: utf-8 -*-
'''
Created on 15.04.2012

@author: moschlar
'''
#TODO: Unified field_order regarding common elements

import logging

from tg import expose, tmpl_context as c, dispatched_controller, request
from tg.decorators import paginate, with_trailing_slash, before_validate
from tgext.crud import CrudRestController, EasyCrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller, FillerBase, EditFormFiller

from sqlalchemy import desc as _desc

from sauce.model import DBSession, Event, Lesson, Team, Student, Sheet, Assignment, Test, Teacher
from sprox.formbase import AddRecordForm, EditableForm

from tw.forms import TextField, BooleanRadioButtonList, SingleSelectField, FileField
from tw.forms.validators import Email, FieldsMatch, Schema
from tw.tinymce import TinyMCE, mce_options_default
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
    
    def __init__(self, filters=[], filter_bys={},
                 menu_items={}, inject={}):
        '''Initialize FilteredCrudRestController with given options'''
        
        # Since DBSession is a scopedsession we don't need to pass it around,
        # so we just use the imported DBSession here
        super(FilteredCrudRestController, self).__init__(DBSession, menu_items)
        
        def custom_do_get_provider_count_and_objs(**kw):
            '''Custom getter function respecting provided filters and filter_bys
            
            Returns the result count from the database and a query object
            
            Mostly stolen from sprox.sa.provider and modified accordingly
            '''
            
            # Get keywords that are not filters
            limit = kw.pop('limit', None)
            offset = kw.pop('offset', None)
            order_by = kw.pop('order_by', None)
            desc = kw.pop('desc', False)
            
            qry = self.model.query
            
            # Process pre-defined filters
            if filters:
                qry = qry.filter(*filters)
            if filter_bys:
                qry = qry.filter_by(**filter_bys)
            
            # Process filters from url
            kwfilters = kw
            kwfilters = self.table_filler.__provider__._modify_params_for_dates(self.model, kwfilters)
            kwfilters = self.table_filler.__provider__._modify_params_for_relationships(self.model, kwfilters)
            
            for field_name, value in kwfilters.iteritems():
                field = getattr(self.model, field_name)
                if self.table_filler.__provider__.is_relation(self.model, field_name) and isinstance(value, list):
                    value = value[0]
                    qry = qry.filter(field.contains(value))
                else: 
                    qry = qry.filter(field==value) 
            
            # Get total count
            count = qry.count()
            
            # Process ordering
            if order_by is not None:
                field = getattr(self.model, order_by)
                if desc:
                    field = _desc(field)
                qry = qry.order_by(field)
            
            # Process pager options
            if offset is not None:
                qry = qry.offset(offset)
            if limit is not None:
                qry = qry.limit(limit)
            
            return count, qry
        # Assign custom getter function to table_filler
        self.table_filler._do_get_provider_count_and_objs = custom_do_get_provider_count_and_objs
        
        self.inject = inject
        
    
    @classmethod
    def injector(cls, remainder, params):
        '''Injects the objects from self.inject into params
        
        self.inject has to be a dictionary of key, object pairs
        '''
        # Get currently dispatched controller instance
        #s = dispatched_controller() # Does not work, only returns last statically dispatch controller, but we use _lookup in EventsController
        s = request.controller_state.controller
        
        for i in s.inject:
            params[i] = s.inject[i]

# Register injection hook for POST requests
before_validate(FilteredCrudRestController.injector)(FilteredCrudRestController.post)

#--------------------------------------------------------------------------------

class TeamsCrudController(FilteredCrudRestController):
    
    model = Team
    
    __table_options__ = {
        '__omit_fields__': ['lesson_id'],
        '__field_order__': ['id', 'name', 'lesson', 'students'],
        }
    __form_options__ = {
        '__field_order__': ['id', 'name', 'lesson', 'students'],
        '__field_widget_types__': {'name': TextField},
        }
    
class StudentsCrudController(FilteredCrudRestController):
    
    model = Student
    
    __table_options__ = {
        '__omit_fields__': ['id', 'password', '_password', 'submissions', 'type', 'groups'],
        '__field_order__': ['id', 'user_name', 'display_name', 'email_address', 'teams', 'created'],
        }
    __form_options__ = {
        '__omit_fields__': ['submissions', 'type', 'created', 'groups'],
        '__field_order__': ['id', 'user_name', 'display_name', 'email_address',
                            'teams', 'password', '_password'],
        '__field_widget_types__': {
                                   'user_name': TextField, 'display_name': TextField,
                                   'email_address': TextField,
                                  },
        '__field_widget_args__': {
                                  'user_name': {'help_text': u'Desired user name for login'},
                                  'display_name': {'help_text': u'Full name'},
                                  },
        '__base_validator__': passwordValidator,
        }

class TeachersCrudController(FilteredCrudRestController):
    
    model = Teacher
    
    __table_options__ = {
        '__omit_fields__': ['id', 'password', '_password', 'type', 'groups',
                            'judgements', 'assignments', 'tests', 'sheets', 'news', 'events'],
        '__field_order__': ['id', 'user_name', 'display_name', 'email_address', 'lessons', 'created'],
        }
    __form_options__ = {
        '__omit_fields__': ['submissions', 'type', 'created', 'groups',
                            'judgements', 'assignments', 'tests', 'sheets', 'news', 'events'],
        '__field_order__': ['id', 'user_name', 'display_name', 'email_address',
                            'lessons', 'password', '_password', 'groups'],
        '__field_widget_types__': {
                                   'user_name': TextField, 'display_name': TextField,
                                   'email_address': TextField,
                                  },
        '__field_widget_args__': {
                                  'user_name': {'help_text': u'Desired user name for login'},
                                  'display_name': {'help_text': u'Full name'},
                                  },
        '__base_validator__': passwordValidator,
        }

class LessonsCrudController(FilteredCrudRestController):
    
    model = Lesson
    
    __table_options__ = {
        '__omit_fields__': ['id', 'event_id', 'event', 'teacher_id'],
        '__field_order__': ['lesson_id', 'name', 'teacher', 'teams'],
        }
    __form_options__ = {
        '__omit_fields__': ['event'],
        '__field_order__': ['id', 'lesson_id', 'name', 'teacher', 'teams'],
        '__field_widget_types__': {'name':TextField},
        }
    

class SheetsCrudController(FilteredCrudRestController):
    
    model = Sheet
    
    __table_options__ = {
        '__omit_fields__': ['id', 'description', 'event_id', 'event', 'teacher_id', '_url'],
        '__field_order__': ['sheet_id', 'name', '_start_time', '_end_time',
                            'public', 'teacher'],
        }
    __form_options__ = {
        '__omit_fields__': ['_url', 'teacher'],
        '__field_order__': ['id', 'sheet_id', 'name', 'description',
                            '_start_time', '_end_time', 'public', 'teacher'],
        '__field_widget_types__': {
                                   'name': TextField, 'description': TinyMCE,
                                   'public': BooleanRadioButtonList,
                                  },
        '__field_widget_args__': {
                                  '_start_time':{'default': u'', 'help_text': u'Leave empty to use value from event'},
                                  '_end_time':{'default': u'', 'help_text': u'Leave empty to use value from event'},
                                  'description':{'mce_options':mce_options_default},
                                  'sheet_id': {'help_text': u'This id will be part of the url and has to be unique for the parent event'},
                                 },
        }

class AssignmentsCrudController(FilteredCrudRestController):
    
    model = Assignment
    
    __table_options__ = {
        '__omit_fields__': ['id', 'event_id', '_event', 'teacher_id', 'teacher',
                            '_teacher', 'sheet_id', 'description', 'tests',
                            'submissions', 'show_compiler_msg'],
        '__field_order__': ['sheet', 'assignment_id', 'name',
                            'public', 'timeout', 'allowed_languages',
                            '_start_time', '_end_time'],
        }
    __form_options__ = {
        '__omit_fields__': ['tests', 'submissions', '_event', 'teacher'],
        '__field_order__': ['id', 'sheet', 'assignment_id', 'name', 'description',
                            '_start_time', '_end_time', 'timeout', 'allowed_languages',
                            'show_compiler_msg', 'tests', 'public'],
        '__field_widget_types__': {
                                   'name': TextField, 'description': TinyMCE,
                                   'show_compiler_msg': BooleanRadioButtonList,
                                   'public': BooleanRadioButtonList
                                  },
        '__field_widget_args__': {
                                  'assignment_id': {'help_text': u'Will be part of the url and has to be unique for the parent sheet'},
                                  'description': {'mce_options': mce_options_default},
                                  '_start_time': {'default': u'', 'help_text': u'Leave empty to use value from sheet'},
                                  '_end_time': {'default': u'', 'help_text': u'Leave empty to use value from sheet'},
                                  'timeout': {'help_text': u'Default timeout value for test cases, leave empty for no time limit'},
                                  'show_compiler_msg': {'help_text': u'Show error messages or warnings from the compiler run'},
                                 }
        }

class TestsCrudController(FilteredCrudRestController):
    
    model = Test
    
    __table_options__ = {
        '__omit_fields__': ['id', 'assignment_id', 'input_data', 'output_data', 'separator',
                            'ignore_case', 'ignore_returncode', 'show_partial_match',
                            'splitlines', 'split',
                            'parse_int', 'parse_float', 'sort',
                            'teacher_id', 'teacher', 'testruns'],
        '__field_order__': ['id', 'assignment', 'visible', '_timeout', 'argv',
                            'input_type', 'output_type', 'input_filename', 'output_filename'],
        }
    __form_options__ = {
        '__omit_fields__': ['testruns', 'teacher'],
        '__field_order__': ['id', 'assignment', 'visible', '_timeout', 'argv',
                            'input_type', 'output_type', 'input_filename', 'output_filename',
                            'input_data', 'output_data', 'separator',
                            'ignore_case', 'ignore_returncode', 'show_partial_match', 'splitlines', 'split',
                            'parse_int', 'parse_float', 'sort'],
        '__field_widget_types__': {
                                   'argv': TextField,
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
        '__field_widget_args__': {
                                  'argv': {'help_text': u'Command line parameters for the test run. Available variables are: {infile} {outfile}'},
                                  'visible': {'help_text': u'Whether test is shown to users or not'},
                                  '_timeout': {'help_text': u'Timeout value, leave empty to use value from assignment'},
                                  'input_type': dict(options=[('stdin','stdin'), ('file','file')]),
                                  'output_type': dict(options=[('stdout','stdout'), ('file','file')]),
                                  'input_data': dict(help_text=u'Warning, this field always overwrites database entries'),
                                  'output_data': dict(help_text=u'Warning, this field always overwrites database entries'),
                                  'separator': {'help_text': u'The separator used for splitting and joining'},
                                 },
        '__field_validator_types__': {
                                      'input_data': FieldStorageUploadConverter,
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
                                 'description': {'mce_options':mce_options_default},
                                }
        }
