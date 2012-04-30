# -*- coding: utf-8 -*-
'''
Created on 15.04.2012

@author: moschlar
'''
#TODO: Unified field_order regarding common elements

import logging

from tg import expose, tmpl_context as c, dispatched_controller, request
from tg.decorators import paginate, with_trailing_slash, before_validate, cached_property
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
    
    @cached_property
    def mount_point(self):
        return '.'
    
    @classmethod
    def injector(cls, remainder, params):
        '''Injects the objects from self.inject into params
        
        self.inject has to be a dictionary of key, object pairs
        '''
        # Get currently dispatched controller instance
        #s = dispatched_controller() # Does not work, only returns last statically dispatch controller, but we use _lookup in EventsController
        s = request.controller_state.controller
        
        if hasattr(s, 'inject'):
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
        '__headers__': {'user_name': 'Username', 'display_name': 'Display name',
                        'email_address': 'E-Mail Address'},
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
                                  'teams': {'help_text': u'These are the teams this student belongs to'},
                                  '_password': {'help_text': u'If you don\'t want to change the password, make this fields empty'},
                                  },
        '__base_validator__': passwordValidator,
        }

class TeachersCrudController(FilteredCrudRestController):
    
    model = Teacher
    
    __table_options__ = {
        '__omit_fields__': ['id', 'password', '_password', 'type', 'groups',
                            'judgements', 'assignments', 'tests', 'sheets', 'news', 'events'],
        '__field_order__': ['id', 'user_name', 'display_name', 'email_address', 'lessons', 'created'],
        '__headers__': {'user_name': 'Username', 'display_name': 'Display name',
                        'email_address': 'E-Mail Address'},
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
                                  'lessons': {'help_text': u'These are the lessons this teacher teaches'},
                                  '_password': {'help_text': u'If you don\'t want to change the password, make this fields empty'},
                                  },
        '__base_validator__': passwordValidator,
        }

#--------------------------------------------------------------------------------

class EventsCrudController(FilteredCrudRestController):
    #TODO: Wrong field_order in form
    
    model = Event
    
    __table_options__ = {
        '__omit_fields__': ['id', 'description', 'teacher_id', 'password',
                            'assignments', 'lessons', 'sheets', 'news',
                           ],
        '__field_order__': ['type', '_url', 'name', 'teacher', 'public',
                            'start_time', 'end_time', 'teachers'],
        '__headers__': {'_url': 'Url',
                        'start_time': 'Start Time', 'end_time': 'End Time'},
        }
    __form_options__ = {
        '__omit_fields__': ['assignments', 'sheets', 'news', 'lessons'],
        '__field_order__': ['type', '_url', 'name', 'description' 'teacher', 'public',
                            'password', 'start_time', 'end_time', 'teachers'],
        '__field_widget_types__': {'name':TextField, 'description':TinyMCE,
                                   'public': BooleanRadioButtonList, '_url':TextField,
                                   'type': SingleSelectField, 'password':TextField,
                                  },
        '__field_widget_args__': {
                                  'type': dict(options=[('course','Course'), ('contest','Contest')]),
                                  'description': {'mce_options':mce_options_default},
                                  '_url': {'help_text': u'Will be part of the url, has to be unique and url-safe'},
                                  'public': {'help_text': u'Make event visible for students'},
                                  'password': {'help_text': u'Password for student self-registration. Currently not implemented'},
                                 }
        }

class LessonsCrudController(FilteredCrudRestController):
    
    model = Lesson
    
    __table_options__ = {
        '__omit_fields__': ['id', 'event_id', 'event', 'teacher_id'],
        '__field_order__': ['lesson_id', 'name', 'teacher', 'teams'],
        '__headers__': {'lesson_id': 'Lesson Id'},
        }
    __form_options__ = {
        '__hide_fields__': ['event'], # If the field is hidden, it does not get validated!
        '__field_order__': ['id', 'lesson_id', 'name', 'teacher', 'teams'],
        '__field_widget_types__': {'name': TextField},
        '__field_widget_args__': {
                                  'lesson_id': {'help_text': u'This id will be part of the url and has to be unique for the parent event'},
                                 },
        }
    

class SheetsCrudController(FilteredCrudRestController):
    
    model = Sheet
    
    __table_options__ = {
        '__omit_fields__': ['id', 'description', 'event_id', 'event',
                            'teacher_id', '_url', '_start_time', '_end_time'],
        '__field_order__': ['sheet_id', 'name', 'public', 'teacher',
                            'start_time', 'end_time'],
        '__headers__': {'sheet_id': 'Sheet Id',
                        'start_time': 'Start Time', 'end_time': 'End Time'},
        }
    __form_options__ = {
        '__omit_fields__': ['_url'],
        '__hide_fields__': ['teacher', 'event'],
        '__field_order__': ['id', 'sheet_id', 'name', 'description',
                            '_start_time', '_end_time', 'public', 'teacher'],
        '__field_widget_types__': {
                                   'name': TextField, 'description': TinyMCE,
                                   'public': BooleanRadioButtonList,
                                  },
        '__field_widget_args__': {
                                  '_start_time':{'default': u'', 'help_text': u'Leave empty to use value from event'},
                                  '_end_time':{'default': u'', 'help_text': u'Leave empty to use value from event'},
                                  'description':{'mce_options': mce_options_default},
                                  'sheet_id': {'help_text': u'This id will be part of the url and has to be unique for the parent event'},
                                  'public': {'help_text': u'Make sheet visible for students'},
                                 },
        }

class AssignmentsCrudController(FilteredCrudRestController):
    
    model = Assignment
    
    __table_options__ = {
        '__omit_fields__': ['id', 'event_id', '_event', 'teacher_id', 'teacher',
                            '_teacher', 'sheet_id', 'description', 'tests',
                            'submissions', 'show_compiler_msg',
                            '_start_time', '_end_time'],
        '__field_order__': ['sheet', 'assignment_id', 'name',
                            'public', 'timeout', 'allowed_languages',
                            'start_time', 'end_time'],
        '__headers__': {'assignment_id': 'Assignment Id', 'allowed_languages': 'Allowed Languages',
                        'start_time': 'Start Time', 'end_time': 'End Time'}
        }
    __form_options__ = {
        '__omit_fields__': ['tests', 'submissions', '_event', '_teacher'],
        '__require_fields__': ['sheet'],
        '__field_order__': ['id', 'sheet', 'assignment_id', 'name', 'description',
                            '_start_time', '_end_time', 'timeout', 'allowed_languages',
                            'show_compiler_msg', 'tests', 'public'],
        '__field_widget_types__': {
                                   'name': TextField, 'description': TinyMCE,
                                   'show_compiler_msg': BooleanRadioButtonList,
                                   'public': BooleanRadioButtonList,
                                  },
        '__field_widget_args__': {
                                  'assignment_id': {'help_text': u'Will be part of the url and has to be unique for the parent sheet'},
                                  'description': {'mce_options': mce_options_default},
                                  '_start_time': {'default': u'', 'help_text': u'Leave empty to use value from sheet'},
                                  '_end_time': {'default': u'', 'help_text': u'Leave empty to use value from sheet'},
                                  'timeout': {'help_text': u'Default timeout value for test cases, leave empty for no time limit'},
                                  'show_compiler_msg': {'help_text': u'Show error messages or warnings from the compiler run'},
                                  'public': {'help_text': u'Make assignment visible for students'},
                                 }
        }

#--------------------------------------------------------------------------------

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
        '__omit_fields__': ['testruns'],
        '__hide_fields__': ['teacher'],
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
                                  'argv': {'help_text': u'''
Command line arguments

Possible variables are:
    {path}: Absolute path to temporary working directory
    {infile}: Full path to test input file
    {outfile}: Full path to test output file
                                  '''},
                                  'visible': {'help_text': u'Whether test is shown to users or not'},
                                  '_timeout': {'help_text': u'Timeout value, leave empty to use value from assignment'},
                                  'input_type': dict(options=[('stdin','stdin'), ('file','file')]),
                                  'output_type': dict(options=[('stdout','stdout'), ('file','file')]),
                                  'input_data': dict(help_text=u'Warning, this field always overwrites database entries'),
                                  'output_data': dict(help_text=u'Warning, this field always overwrites database entries'),
                                  'separator': {'help_text': u'The separator string used for splitting and joining, default is None (whitespace)'},
                                  'ignore_case': {'help_text': u'Call .upper() on output before comparison'},
                                  'ignore_returncode': {'help_text': u'Ignore test process returncode'},
                                  'show_partial_match': {'help_text': u'Recognize partial match and show to user'},
                                  'splitlines': {'help_text': u'Call .splitlines() on full output before comparison'},
                                  'split': {'help_text': u'Call .split() on full output of output before comparison or on each line from .splitlines() if splitlines is set'},
                                  'parse_int': {'help_text': u'Parse every substring in output to int before comparison'},
                                  'parse_float': {'help_text': u'Parse every substring in output to float before comparison'},
                                  'sort': {'help_text': u'''Sort output and test data before comparison
Parsing is performed first, if enabled
Results depends on whether splitlines and/or split are set:
if split and splitlines:
    2-dimensional array in which only the second dimension 
    is sorted (e.g. [[3, 4], [1, 2]])
if only split or only splitlines:
    1-dimensional list is sorted by the types default comparator
    '''},
                                 },
        '__field_validator_types__': {
                                      'input_data': FieldStorageUploadConverter,
                                      'output_data': FieldStorageUploadConverter,
                                     },
        }
