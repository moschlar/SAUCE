# -*- coding: utf-8 -*-
'''
Created on 12.11.2012

@author: moschlar
'''

import logging

import tw2.tinymce as twt
import tw2.bootstrap.forms as twb
from webhelpers.html.tags import link_to

from sauce.model import Sheet, Assignment

from sauce.controllers.crc.base import FilteredCrudRestController

__all__ = ['SheetsCrudController', 'AssignmentsCrudController']

log = logging.getLogger(__name__)


class SheetsCrudController(FilteredCrudRestController):

    model = Sheet

    __table_options__ = {
        '__omit_fields__': ['id', 'description', 'event_id', 'event', 'teacher',
                            '_teacher', 'teacher_id', '_url', '_start_time', '_end_time'],
        '__field_order__': ['sheet_id', 'name', 'public',
                            'start_time', 'end_time', 'assignments'],
        '__search_fields__': ['id', 'sheet_id', 'name', ('assignments', 'assignment_id')],
        '__xml_fields__': ['assignments'],
        'start_time': lambda filler, obj: obj.start_time.strftime('%x %X'),
        'end_time': lambda filler, obj: obj.end_time.strftime('%x %X'),
        'assignments': lambda filler, obj: ', '.join(link_to(ass.name, '../assignments/%d/edit' % ass.id) for ass in obj.assignments),
        '__base_widget_args__': {'sortList': [[1, 0]]},
        }
    __form_options__ = {
        '__omit_fields__': ['id', '_url', 'assignments', 'teacher', '_teacher'],
        '__hide_fields__': ['event'],
        '__field_order__': ['id', 'sheet_id', 'name', 'description',
                            'public', '_start_time', '_end_time'],
        '__field_widget_types__': {
                                   'name': twb.TextField, 'description': twt.TinyMCEWidget,
                                  },
        '__field_widget_args__': {
                                  '_start_time': {'help_text': u'Leave empty to use value from event',
                                      'default': u'', 'date_format': '%d.%m.%Y %H:%M'},
                                  '_end_time': {'help_text': u'Leave empty to use value from event',
                                      'default': u'', 'date_format': '%d.%m.%Y %H:%M'},
                                  'description': {'css_class': 'span6'},
                                  #'description':{'mce_options': mce_options_default},
                                  'sheet_id': {'label': u'Sheet Id', 'help_text': u'This id will be part of the url and has to be unique for the parent event'},
                                  'public': {'help_text': u'Make sheet visible for students', 'default': True},
                                  #'assignments': {'size': 10},
                                 },
        '__require_fields__': ['sheet_id'],
        }


class AssignmentsCrudController(FilteredCrudRestController):

    model = Assignment

    __table_options__ = {
        '__omit_fields__': ['id', 'event_id', '_event', '_url',
                            'teacher_id', 'teacher', 'allowed_languages',
                            '_teacher', 'description', 'tests',
                            'submissions', 'show_compiler_msg',
                            '_start_time', '_end_time'],
        '__field_order__': ['sheet_id', 'sheet', 'assignment_id', 'name',
                            'public', 'start_time', 'end_time',
                            'timeout'],
        '__search_fields__': ['id', 'sheet_id', 'assignment_id', 'name'],
        '__xml_fields__': ['sheet'],
        'start_time': lambda filler, obj: obj.start_time.strftime('%x %X'),
        'end_time': lambda filler, obj: obj.end_time.strftime('%x %X'),
        'sheet': lambda filler, obj: link_to(obj.sheet.name, '../sheets/%d/edit' % obj.sheet.id),
        '__base_widget_args__': {'sortList': [[1, 0], [3, 0]]},
        }
    __form_options__ = {
        '__omit_fields__': ['id', 'tests', 'submissions', '_event', 'teacher', '_url', '_teacher'],
        '__field_order__': ['id', 'sheet', 'assignment_id', 'name', 'description',
                            'public', '_start_time', '_end_time',
                            'timeout', 'allowed_languages', 'show_compiler_msg'],
        '__field_widget_types__': {
                                   'name': twb.TextField, 'description': twt.TinyMCEWidget,
                                  },
        '__field_widget_args__': {
                                  'assignment_id': {'label': u'Assignment Id', 'help_text': u'Will be part of the url and has to be unique for the parent sheet'},
                                  'description': {'css_class': 'span6'},
                                  '_start_time': {'help_text': u'Leave empty to use value from event',
                                      'default': u'', 'date_format': '%d.%m.%Y %H:%M'},
                                  '_end_time': {'help_text': u'Leave empty to use value from event',
                                      'default': u'', 'date_format': '%d.%m.%Y %H:%M'},
                                  'timeout': {'help_text': u'Default timeout value for test cases, leave empty for no time limit'},
                                  'allowed_languages': {'size': 6},
                                  'show_compiler_msg': {'help_text': u'Show error messages or warnings from the compiler run', 'default': True},
                                  'public': {'help_text': u'Make assignment visible for students', 'default': True},
                                 },
        '__require_fields__': ['assignment_id',
                               'sheet',
                               ],
        '__base_widget_type__': twb.HorizontalForm,
        }
