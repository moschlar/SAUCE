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

from tg import lurl

from sauce.controllers.crc.base import FilterCrudRestController
from sauce.model import Test

import tw2.bootstrap.forms as twb
import tw2.jqplugins.chosen.widgets as twjc
try:
    from tw2.ace import AceWidget as SourceEditor
#    from tw2.codemirror import CodeMirrorWidget as SourceEditor
except ImportError:
    from tw2.bootstrap.forms import TextArea as SourceEditor

from webhelpers.html.tags import link_to

import logging
log = logging.getLogger(__name__)

__all__ = ['TestsCrudController']


class TestsCrudController(FilterCrudRestController):

    model = Test

    __table_options__ = {
        '__omit_fields__': [
            'argv',
            'input_data', 'output_data',
            'input_filename', 'output_filename',
            'ignore_case', 'ignore_returncode', 'show_partial_match',
            'splitlines', 'split', 'comment_prefix',
            'separator',
            'failsafe_parsing',
            'parse_int', 'parse_float', 'float_precision',
            'sort',
            'user_id', 'user', 'testruns',
        ],
        '__field_order__': [
            'id', 'assignment_id', 'assignment', 'name', 'visible', '_timeout',
            'input_type', 'output_type',
        ],
        '__search_fields__': ['id', 'assignment_id', 'name'],
#        '__headers__': {'_timeout': 'Timeout'},
        '__xml_fields__': ['assignment'],
        'assignment': lambda filler, obj: \
            link_to(obj.assignment.name, '../assignments/%d/edit' % obj.assignment.id),
        '__base_widget_args__': {'sortList': [[2, 0], [1, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': ['id', 'testruns'],
        '__hide_fields__': ['user'],
        '__add_fields__': {
            'docs': twb.Label('docs', text='Please read the <a href="%s">' % lurl('/docs/tests') +
                'Test configuration documentation</a>!', css_class='bold', escape=False),
            'ignore_opts': twb.Label('ignore_opts', text='Output ignore options', css_class='label'),
            'split_opts': twb.Label('split_opts', text='Output splitting options', css_class='label'),
            'parse_opts': twb.Label('parse_opts', text='Output parsing options', css_class='label'),
        },
        '__field_order__': [
            'id', 'docs', 'assignment',
            'name', 'visible',
            'result_public', 'data_public',
            'input_data', 'output_data',
            'input_type', 'output_type',
            'input_filename', 'output_filename',
            '_timeout', 'argv',
            'ignore_opts',
            'ignore_case', 'comment_prefix', 'ignore_returncode', 'show_partial_match',
            'split_opts',
            'splitlines', 'split', 'separator', 'sort',
            'parse_opts',
            'failsafe_parsing',
            'parse_int', 'parse_float', 'float_precision',
        ],
        '__field_widget_types__': {
#             'name': twb.TextField,
            'argv': twb.TextField,
            'input_filename': twb.TextField,
            'output_filename': twb.TextField,
            'input_type': twjc.ChosenSingleSelectField,
            'output_type': twjc.ChosenSingleSelectField,
#             'input_data': FileField,
#             'output_data': FileField,
            'input_data': SourceEditor,
            'output_data': SourceEditor,
        },
        '__field_widget_args__': {
            'argv': {'help_text': u'''
Command line arguments

Possible variables are:
    {path}: Absolute path to temporary working directory
    {infile}: Full path to test input file
    {outfile}: Full path to test output file'''
            },
            'visible': {'help_text': u'Whether test is shown to users or not', 'default': True},
            '_timeout': {'help_text': u'Timeout value, leave empty to use value from assignment'},
            'input_type': dict(options=[('stdin', 'stdin'), ('file', 'file')], value='stdin', prompt_text=None),
            'output_type': dict(options=[('stdout', 'stdout'), ('file', 'file')], value='stdout', prompt_text=None),
            'input_data': dict(css_class='span7', cols=80, rows=6),
            'output_data': dict(css_class='span7', cols=80, rows=6),
            'input_filename': dict(css_class='span7'),
            'output_filename': dict(css_class='span7'),
            'argv': dict(css_class='span7'),
            'separator': {'help_text': u'The separator string used for splitting and joining, default is None (whitespace)'},
            'ignore_case': {'help_text': u'Call .lower() on output before comparison', 'default': True},
            'ignore_returncode': {'help_text': u'Ignore test process returncode', 'default': True},
            'comment_prefix': {'help_text': u'Ignore all lines that start with comment_prefix'},
            'show_partial_match': {'help_text': u'Recognize partial match and show to user', 'default': True},
            'splitlines': {'help_text': u'Call .splitlines() on full output before comparison', 'default': False},
            'split': {'help_text': u'Call .split() on full output of output before comparison or on each line from .splitlines() if splitlines is set'},
            'failsafe_parsing': {'help_text': u'Leave unparsable fragments as they are or strip them out'},
            'parse_int': {'help_text': u'Parse every substring in output to int before comparison', 'default': False},
            'parse_float': {'help_text': u'Parse every substring in output to float before comparison', 'default': False},
            'float_precision': {'help_text': u'''The precision (number of decimal digits) to compare for floats'''},
            'sort': {'help_text': u'''Sort output and test data before comparison
Parsing is performed first, if enabled
Results depends on whether splitlines and/or split are set:
if split and splitlines:
    2-dimensional array in which only the second dimension
    is sorted (e.g. [[3, 4], [1, 2]])
if only split or only splitlines:
    1-dimensional list is sorted by the types default comparator
    ''', 'default': False},
        },
    }
