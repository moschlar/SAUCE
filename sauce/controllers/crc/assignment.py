# -*- coding: utf-8 -*-
'''CrudControllers for Sheet and Assignment entities

@see: :mod:`sauce.controllers.crc.base`

TODO: If possible, syntax highlighting for scaffold and template
TODO: tw2.dynforms to display scaffold field conditionally

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

import logging
from itertools import groupby

from webhelpers.html.tags import link_to, literal

from tg import config, expose, flash, redirect, request, tmpl_context as c, url

import tw2.bootstrap.forms as twb

import sauce.lib.helpers as h
from sauce.controllers.crc.base import FilterCrudRestController
from sauce.controllers.crc.test import run_tests
from sauce.model import Assignment, Event, Sheet
from sauce.widgets.copy import CopyForm
from sauce.widgets.widgets import MediumSourceEditor


log = logging.getLogger(__name__)

__all__ = ['SheetsCrudController', 'AssignmentsCrudController']


_lti = config.features.get('lti', False)


#--------------------------------------------------------------------------------

def _submissions(filler, obj):
    '''Display submission link button for Assignments or Sheets'''
    return (u'<a href="%s/submissions" style="white-space: pre;" class="btn btn-mini">'
        '<i class="icon-inbox"></i>&nbsp;Submissions</a>' % (obj.url))

#--------------------------------------------------------------------------------


class SheetsCrudController(FilterCrudRestController):
    '''CrudController for Sheets'''

    model = Sheet

    __table_options__ = {
        '__omit_fields__': [
            'id', 'description', 'event_id', 'event', 'teacher',
            '_teacher', 'teacher_id', '_url', '_start_time', '_end_time',
        ],
        '__field_order__': [
            'sheet_id', 'name', 'public',
            'start_time', 'end_time', 'assignments',
            'submissions',
        ],
        '__search_fields__': ['id', 'sheet_id', 'name', ('assignments', 'assignment_id')],
        '__xml_fields__': ['sheet_id', 'name', 'assignments', 'submissions'],
        '__headers__': {'sheet_id': ''},
        'start_time': lambda filler, obj: h.strftime(obj.start_time, False),
        'end_time': lambda filler, obj: h.strftime(obj.end_time, False),
        'sheet_id': lambda filler, obj:
            literal(u'<span title="sheet_id=%d">%d</span>' % (obj.sheet_id, obj.sheet_id)),
        'name': lambda filler, obj:
            literal(u'<span title="sheet_id=%d">%s</span>' % (obj.sheet_id, obj.name)),
        'assignments': lambda filler, obj:
            ', '.join(link_to(ass.name, '../assignments/%d/edit' % ass.id)
                for ass in obj.assignments) + (
                '&nbsp;' +
                u'<a href="%s/copy" class="btn btn-mini" title="Copy Assignment">'
                '<i class="icon-share-alt"></i></a>' % (obj.id)),
        'submissions': _submissions,
        '__base_widget_args__': {'sortList': [[1, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': [
            'id', '_url', 'assignments', 'teacher', '_teacher',
        ],
        '__hide_fields__': ['event'],
        '__field_order__': [
            'id', 'sheet_id', 'name', 'description',
            'public', '_start_time', '_end_time',
        ],
        '__field_widget_args__': {
            '_start_time': {
                'help_text': u'Leave empty to inherit from the parent event',
            },
            '_end_time': {
                'help_text': u'Leave empty to inherit from the parent event',
            },
            'sheet_id': {
                'label': u'Sheet id',
                'help_text': u'This id will be part of the url and has to be unique within the parent event',
            },
            'public': {
                'help_text': u'Make sheet visible for students',
            },
        },
        '__require_fields__': ['sheet_id'],
    }
    __setters__ = {
        'test': ('null', lambda sheet:
            run_tests((submission for assignment in sheet.assignments for submission in assignment.submissions))),
    }

    def _actions(self, obj):
        actions = super(SheetsCrudController, self)._actions(obj)
        actions.insert(1, u'''
<a href="%d/test" class="btn btn-mini btn-inverse" title="Re-run all tests for this sheet"
    onclick="show_processing_modal('Testing %d Submission(s) in %d Test(s)...'); return true;">
    <i class="icon-repeat icon-white"></i>
</a>''' % (obj.id, sum((len(assignment.submissions) for assignment in obj.assignments)),
    sum((len(assignment.submissions) * len(assignment.tests) for assignment in obj.assignments))))
        return actions

    parent_model = Event
    child_model = Assignment

    def _self_copy_options(self):
        for e, ss in groupby(self.model.query.order_by('event_id'), lambda s: s.event):
            yield (e.name, [(s.id, s.name) for s in ss])

    def _child_copy_options(self, parent):
        for s,aa in groupby(self.child_model.query.order_by('sheet_id'), lambda a: a.sheet):
            yield (u'%s &mdash; %s' % (s.event.name, s.name), [(a.id, a.name) for a in aa])

    @expose('sauce.templates.form')
    # XXX: This is really really hacky...
    # TODO: Logging
    def copy(self, *args, **kwargs):
        # print self, args, kwargs
        if not self.allow_copy:
            abort(status.HTTP_403_FORBIDDEN)
        # print self.model, self.child_model

        if args:
            parent_model = self.model
            child_model = self.child_model
            key = 'assignment_id'
            parent = self.model.query.get(*args)
            # print parent
            options = list(self._child_copy_options(parent))
            heading = u'Clone %s to %s' % (self.child_model.__name__.capitalize(), parent)
            return_url = '..'
        else:
            parent_model = self.parent_model
            child_model = self.model
            key = 'sheet_id'
            parent = dict(request.controller_state.controller_path)['admin'].event
            # print parent
            options = list(self._self_copy_options())
            heading = u'Clone %s to %s' % (self.model.__name__.capitalize(), parent)
            return_url = '.'

        if kwargs:
            child = child_model.query.get(kwargs['selection'])
            # print child
            i = max(getattr(p, key) for p in parent.children) if parent.children else 0
            # print i
            clone = child.clone(i=i, recursive=True)
            # print clone
            # print parent.children
            parent.children.append(clone)
            # print parent.children
            flash('Successfully cloned %r from %r' % (clone, child), 'ok')
            redirect(return_url)

        # c.text = repr(options)
        flash(u'Be advised that this feature is highly experimental!', 'warn')
        c.text = u'This feature will always create recursive copies (e.g. Sheets include Assignments include Tests)!'
        c.form = CopyForm(options=options, method='get')
        return dict(page='clone', heading=heading)


class AssignmentsCrudController(FilterCrudRestController):
    '''CrudController for Assignments'''

    model = Assignment

    __table_options__ = {
        '__omit_fields__': [
            'id', 'event_id', '_event', '_url',
            'teacher_id', 'teacher',
            #'allowed_languages',
            '_teacher', 'description',
            'show_compiler_msg',
            '_start_time', '_end_time',
            'submission_filename', 'submission_template',
            'submission_scaffold_show',
            'submission_scaffold_head', 'submission_scaffold_foot',
            '_lti',
        ],
        '__field_order__': [
            'sheet_id', 'sheet', 'assignment_id', 'name',
            'public', 'start_time', 'end_time',
            'timeout', 'allowed_languages',
            'tests',
            'submissions',
        ] + (['lti_url'] if _lti else []),
        '__search_fields__': ['id', 'sheet_id', 'assignment_id', 'name'],
        '__xml_fields__': ['name', 'sheet_id', 'assignment_id', 'sheet',
            'allowed_languages', 'tests', 'submissions', 'lti_url'],
        '__headers__': {
            'sheet_id': '',
            'assignment_id': '',
        },
        'start_time': lambda filler, obj: h.strftime(obj.start_time, False),
        'end_time': lambda filler, obj: h.strftime(obj.end_time, False),
        'name': lambda filler, obj:
            literal(u'<span title="assignment_id=%d">%s</span>' % (obj.assignment_id, obj.name)),
        'sheet_id': lambda filler, obj:
            literal(u'<span title="sheet_id=%d">%d</span>' % (obj.sheet_id, obj.sheet_id)),
        'assignment_id': lambda filler, obj:
            literal(u'<span title="assignment_id=%d">%d</span>' % (obj.assignment_id, obj.assignment_id)),
        'sheet': lambda filler, obj:
            link_to(obj.sheet.name, '../sheets/%d/edit' % obj.sheet.id, title='sheet_id=%d' % (obj.sheet_id)),
        'allowed_languages': lambda filler, obj:
            ', '.join(link_to(l.name, '/languages/%d' % l.id)
                for l in obj.allowed_languages),
        'lti_url': lambda filler, obj:
            u'<span title="%s:%s">%s</span>' % (obj.lti.oauth_key, obj.lti.oauth_secret,
                url(obj.lti_url, qualified=True)) if obj.lti else u'',
        'submissions': _submissions,
        'tests': lambda filler, obj:
            literal(u'<a href="../tests/?assignment_id=%d" class="badge">%d</a> '
                    u'<a href="../tests/new?assignment=%d" class="btn btn-mini">'
                    u'<i class="icon-plus-sign"></i></a>' % (obj.id, len(obj.tests), obj.id)),
        '__base_widget_args__': {'sortList': [[1, 0], [3, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': [
            'id', 'tests', 'submissions', '_event', 'teacher', '_url', '_teacher',
            '_lti',
        ],
        '__add_fields__': {
            'submission_note': twb.Label('submission_note', label='Note', css_class='bold',
                text='For obvious reasons, it might not be the best idea to '
                    'pre-define submission data here, '
                    'when multiple languages are allowed.'),
        },
        '__field_order__': [
            'id', 'sheet', 'assignment_id', 'name', 'description',
            'public', '_start_time', '_end_time',
            'timeout', 'allowed_languages', 'show_compiler_msg',
            'submission_note',
            'submission_filename', 'submission_template',
            'submission_scaffold_show',
            'submission_scaffold_head', 'submission_scaffold_foot',
        ],
        '__field_widget_types__': {
            'submission_template': MediumSourceEditor,
            'submission_scaffold_head': MediumSourceEditor,
            'submission_scaffold_foot': MediumSourceEditor,
        },
        '__field_widget_args__': {
            'assignment_id': {
                'label': u'Assignment id',
                'help_text': u'This id will be part of the url and has to be unique within the parent sheet',
            },
            'public': {
                'help_text': u'Make assignment visible for students',
            },
            '_start_time': {
                'help_text': u'Leave empty to inherit from the parent sheet',
            },
            '_end_time': {
                'help_text': u'Leave empty to inherit from the parent sheet',
            },
            'timeout': {
                'help_text': u'Default timeout value for test cases, leave empty for no time limit',
            },
            'show_compiler_msg': {
                'help_text': u'Show error messages or warnings from the compiler run',
            },
            'submission_filename': {
                'help_text': u'Default filename for submission',
            },
            'submission_template': {
                'help_text': u'Template for submission source body',
            },
            'submission_scaffold_show': {
                'help_text': u'Whether to show head and foot scaffold to student',
            },
            'submission_scaffold_head': {
                'help_text': u'Enforced head for submission source',
            },
            'submission_scaffold_foot': {
                'help_text': u'Enforced foot for submission source',
            },
        },
        '__require_fields__': ['assignment_id', 'sheet'],
    }
    __setters__ = {
        'test': ('null', lambda assignment: run_tests(assignment.submissions)),
    }

    def _actions(self, obj):
        actions = super(AssignmentsCrudController, self)._actions(obj)
        actions.insert(1, u'''
<a href="%d/test" class="btn btn-mini btn-inverse" title="Re-run all tests for this assignment"
    onclick="show_processing_modal('Testing %d Submission(s) in %d Test(s)...'); return true;">
    <i class="icon-repeat icon-white"></i>
</a>''' % (obj.id, len(obj.submissions), len(obj.submissions) * len(obj.tests)))
        return actions
