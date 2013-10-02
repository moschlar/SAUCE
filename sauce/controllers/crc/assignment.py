# -*- coding: utf-8 -*-
'''
Created on 12.11.2012

@author: moschlar
'''
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
from sauce.model import Sheet, Assignment
import sauce.lib.helpers as h

from webhelpers.html.tags import link_to

import logging
log = logging.getLogger(__name__)

__all__ = ['SheetsCrudController', 'AssignmentsCrudController']


class SheetsCrudController(FilterCrudRestController):

    model = Sheet

    __table_options__ = {
        '__omit_fields__': [
            'id', 'description', 'event_id', 'event', 'teacher',
            '_teacher', 'teacher_id', '_url', '_start_time', '_end_time',
        ],
        '__field_order__': [
            'sheet_id', 'name', 'public',
            'start_time', 'end_time', 'assignments',
        ],
        '__search_fields__': ['id', 'sheet_id', 'name', ('assignments', 'assignment_id')],
        '__xml_fields__': ['assignments'],
        'start_time': lambda filler, obj: h.strftime(obj.start_time, False),
        'end_time': lambda filler, obj: h.strftime(obj.end_time, False),
        'assignments': lambda filler, obj: \
            ', '.join(link_to(ass.name, '../assignments/%d/edit' % ass.id) \
                for ass in obj.assignments),
        '__base_widget_args__': {'sortList': [[1, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': ['id', '_url', 'assignments', 'teacher', '_teacher'],
        '__hide_fields__': ['event'],
        '__field_order__': [
            'id', 'sheet_id', 'name', 'description',
            'public', '_start_time', '_end_time',
        ],
        '__field_widget_args__': {
            '_start_time': {
                'help_text': u'Leave empty to use value from event',
            },
            '_end_time': {
                'help_text': u'Leave empty to use value from event',
            },
            'sheet_id': {
                'label': u'Sheet Id',
                'help_text': u'This id will be part of the url and has to be unique for the parent event',
            },
            'public': {
                'help_text': u'Make sheet visible for students',
            },
        },
        '__require_fields__': ['sheet_id'],
    }


class AssignmentsCrudController(FilterCrudRestController):

    model = Assignment

    __table_options__ = {
        '__omit_fields__': [
            'id', 'event_id', '_event', '_url',
            'teacher_id', 'teacher',
            #'allowed_languages',
            '_teacher', 'description', 'tests',
            'submissions', 'show_compiler_msg',
            '_start_time', '_end_time',
        ],
        '__field_order__': [
            'sheet_id', 'sheet', 'assignment_id', 'name',
            'public', 'start_time', 'end_time',
            'timeout', 'allowed_languages',
        ],
        '__search_fields__': ['id', 'sheet_id', 'assignment_id', 'name'],
        '__xml_fields__': ['sheet', 'allowed_languages'],
        'start_time': lambda filler, obj: h.strftime(obj.start_time, False),
        'end_time': lambda filler, obj: h.strftime(obj.end_time, False),
        'sheet': lambda filler, obj: \
            link_to(obj.sheet.name, '../sheets/%d/edit' % obj.sheet.id),
        'allowed_languages': lambda filler, obj: \
            ', '.join(link_to(l.name, '/languages/%d' % l.id) \
                for l in obj.allowed_languages),
        '__base_widget_args__': {'sortList': [[1, 0], [3, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': ['id', 'tests', 'submissions', '_event', 'teacher', '_url', '_teacher'],
        '__field_order__': [
            'id', 'sheet', 'assignment_id', 'name', 'description',
            'public', '_start_time', '_end_time',
            'timeout', 'allowed_languages', 'show_compiler_msg',
        ],
        '__field_widget_args__': {
            'assignment_id': {
                'label': u'Assignment Id',
                'help_text': u'Will be part of the url and has to be unique for the parent sheet',
            },
            '_start_time': {
                'help_text': u'Leave empty to use value from sheet',
            },
            '_end_time': {
                'help_text': u'Leave empty to use value from sheet',
            },
            'timeout': {
                'help_text': u'Default timeout value for test cases, leave empty for no time limit',
            },
            'show_compiler_msg': {
                'help_text': u'Show error messages or warnings from the compiler run',
            },
            'public': {
                'help_text': u'Make assignment visible for students',
            },
        },
        '__require_fields__': ['assignment_id', 'sheet'],
    }
