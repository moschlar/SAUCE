# -*- coding: utf-8 -*-
'''CrudControllers for Test entities

Due to the many options on Test entities, this controllers looks like a mess.

@see: :mod:`sauce.controllers.crc.base`

@since: 12.11.2012

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

from tg import lurl, flash

from sauce.controllers.crc.base import FilterCrudRestController
from sauce.model import Test

import tw2.bootstrap.forms as twb
import tw2.jqplugins.chosen.widgets as twjc
from sauce.widgets.widgets import SmallSourceEditor

from webhelpers.html.tags import literal, link_to

import logging
log = logging.getLogger(__name__)

__all__ = ['TestsCrudController']


def run_tests(submissions):
    r, s, f = 0, 0, 0
    for submission in submissions:
        _, _, rr = submission.run_tests()
        r += 1
        if rr:
            s += 1
        else:
            f += 1
#     r = [submission.run_tests() for submission in submissions]
    flash('%d Submission(s) tested: Successful: %d - Failed: %d' % (r, s, f), 'info')
    return True


class TestsCrudController(FilterCrudRestController):
    '''CrudController for Tests'''

    model = Test

    __table_options__ = {
        '__omit_fields__': [
            'assignment_id',
            'argv',
            '_visible',
            'input_data', 'output_data',
            'input_filename', 'output_filename',
            'ignore_case', 'ignore_returncode', 'show_partial_match',
            'splitlines', 'split', 'comment_prefix',
            'separator',
            'strip_parse_errors',
            'parse_int', 'parse_float', 'float_precision',
            'sort',
            'user_id', 'user', 'testruns',
        ],
        '__field_order__': [
            'id', 'assignment',
            'name', 'visibility',
            '_timeout',
            'input_type', 'output_type',
        ],
        '__search_fields__': ['id', 'assignment_id', 'name'],
        # '__headers__': {'_timeout': 'Timeout'},
        '__xml_fields__': ['assignment'],
        'assignment': lambda filler, obj:
            literal(u'''<a href="%d/test" class="btn btn-mini btn-inverse" title="Re-run all tests for this assignment"
                onclick="show_processing_modal('Testing %d Submission(s) in %d Test(s)...'); return true;">
                <i class="icon-repeat icon-white"></i>
            </a>&nbsp;''' % (obj.id, len(obj.assignment.submissions), len(obj.assignment.submissions) * len(obj.assignment.tests))) +
            link_to(obj.assignment.name, '../assignments/%d/edit' % obj.assignment.id, title='assignment_id=%d' % (obj.assignment_id)),
        '__base_widget_args__': {'sortList': [[1, 0], [2, 0], [3, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': ['id', 'testruns', '_visible'],
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
            'name', 'visibility',
            'input_data', 'output_data',
            'input_type', 'output_type',
            'input_filename', 'output_filename',
            '_timeout', 'argv',
            'ignore_opts',
            'ignore_case', 'comment_prefix', 'ignore_returncode', 'show_partial_match',
            'split_opts',
            'splitlines', 'split', 'separator', 'sort',
            'parse_opts',
            'strip_parse_errors',
            'parse_int', 'parse_float', 'float_precision',
        ],
        '__field_widget_types__': {
            # 'name': twb.TextField,
            'argv': twb.TextField,
            'input_filename': twb.TextField,
            'output_filename': twb.TextField,
            'input_type': twjc.ChosenSingleSelectField,
            'output_type': twjc.ChosenSingleSelectField,
            'visibility': twb.RadioButtonTable,
            # 'input_data': FileField,
            # 'output_data': FileField,
            'input_data': SmallSourceEditor,
            'output_data': SmallSourceEditor,
        },
        '__field_widget_args__': {
            'argv': {
                'help_text': u'''
Command line arguments

Possible variables are:
    {path}: Absolute path to temporary working directory
    {infile}: Full path to test input file
    {outfile}: Full path to test output file'''
            },
            'visibility': {
                'id': 'visibility',
                'name': 'visibility',
                'help_text': u'Whether testrun results and/or data is shown to students or not',
                'prompt_text': None,
                'cols': 2,
                'options': [
                    ('visible', 'Visible'),
                    ('invisible', 'Invisible'),
                    ('result_only', 'Show only the testrun result'),
                    ('data_only', 'Show only the testrun data'),
                ],
                'value': 'visible',
            },
            '_timeout': {
                'help_text': u'Timeout value, leave empty to inherit from the parent assignment',
            },
            'input_type': {
                'prompt_text': None,
                'options': [('stdin', 'stdin'), ('file', 'file')],
                'value': 'stdin',
            },
            'output_type': {
                'prompt_text': None,
                'options': [('stdout', 'stdout'), ('file', 'file')],
                'value': 'stdout',
            },
            'input_filename': {'css_class': 'span7'},
            'output_filename': {'css_class': 'span7'},
            'argv': {'css_class': 'span7'},
            'separator': {
                'help_text': u'The separator string used for splitting and joining, default is None (whitespace)',
            },
            'ignore_case': {
                'help_text': u'Call .lower() on output before comparison',
                'default': True,
            },
            'ignore_returncode': {
                'help_text': u'Ignore test process returncode',
                'default': True,
            },
            'comment_prefix': {
                'help_text': u'Ignore all lines that start with comment_prefix',
            },
            'show_partial_match': {
                'help_text': u'Recognize partial match and show to user',
                'default': True,
            },
            'splitlines': {
                'help_text': u'Call .splitlines() on full output before comparison',
                'default': False,
            },
            'split': {
                'help_text': u'Call .split() on full output of output before comparison or on each line from .splitlines() if splitlines is set',
            },
            'strip_parse_errors': {
                'help_text': u'Strip (True) or leave (False) unparsed fragments',
            },
            'parse_int': {
                'help_text': u'Parse every substring in output to int before comparison',
                'default': False,
            },
            'parse_float': {
                'help_text': u'Parse every substring in output to float before comparison',
                'default': False,
            },
            'float_precision': {
                'help_text': u'''The precision (number of decimal digits) to compare for floats''',
            },
            'parallel_sort': {
                'help_text': u'''If set, output will be sorted with the help of the thread ID inside of '[]' ''',
            },
            'sort': {
                'help_text': u'''Sort output and test data before comparison. Parsing is performed first, if enabled.''',
                'default': False,
            },
        },
    }
    __setters__ = {
        'test': ('null', lambda test: run_tests(test.assignment.submissions)),
    }
