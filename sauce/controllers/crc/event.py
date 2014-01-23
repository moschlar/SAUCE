# -*- coding: utf-8 -*-
'''CrudControllers for Event and Lesson entities

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

from sauce.controllers.crc.base import FilterCrudRestController
from sauce.model import Event, Lesson
from sauce.widgets.widgets import MediumTextField
import sauce.lib.helpers as h

import tw2.core as twc
import tw2.bootstrap.forms as twb
import tw2.jqplugins.chosen.widgets as twjc
from formencode.validators import PlainText
from webhelpers.html.tags import link_to

import logging
log = logging.getLogger(__name__)

__all__ = ['EventsCrudController', 'LessonsCrudController']


class EventsCrudController(FilterCrudRestController):
    '''CrudController for Events

    TODO: Use tw2.dynforms to only display password field when enroll is not None
    '''

    model = Event

    __table_options__ = {
        '__omit_fields__': [
            'id', 'description', 'password',
            '_teacher', '_teacher_id',
            '_assignments', 'lessons', 'sheets', 'news',
            'lti',
        ],
        '__field_order__': [
            'type', '_url', 'name', 'public',
            'start_time', 'end_time',
            'teachers', 'tutors', '_members',
        ],
        '__search_fields__': ['id', '_url', 'name'],
        # '__headers__': {'_url': 'Url'},
        '__xml_fields__': ['teachers', 'tutors'],
        'start_time': lambda filler, obj: h.strftime(obj.start_time, False),
        'end_time': lambda filler, obj: h.strftime(obj.end_time, False),
        'teachers': lambda filler, obj:
            ', '.join(link_to(teacher.display_name, '../tutors/%d/edit' % teacher.id)
                for teacher in set(obj.teachers)),
        'tutors': lambda filler, obj:
            ', '.join(link_to(tutor.display_name, '../tutors/%d/edit' % tutor.id)
                for tutor in obj.tutors),
        '_members': lambda filler, obj:
            ', '.join(link_to(student.display_name, '../students/%d/edit' % student.id)
                for student in obj._members),
        '__base_widget_args__': {'sortList': [[6, 1], [5, 1]]},
    }
    __form_options__ = {
        '__omit_fields__': [
            'id', 'type', '_assignments', 'sheets', 'news', 'lessons',
            '_teacher', '_teacher_id',
            'lti',
        ],
        '__field_order__': [
            'id', '_url', 'name', 'description',
            'public', 'enroll', 'password',
            'start_time', 'end_time',
            'teachers', '_members',
        ],
        '__field_widget_types__': {
            'type': twjc.ChosenSingleSelectField,
            'enroll': twb.RadioButtonTable,
            'password': MediumTextField,
        },
        '__field_widget_args__': {
            '_url': {
                'help_text': u'Will be part of the url, has to be unique and url-safe',
            },
            'public': {
                'help_text': u'Make event visible for students',
            },
            'enroll': {
                'name': 'enroll', 'id': 'enroll',
                'cols': 3,
                'options': [
                    ('', 'None'), ('event', 'Event'), ('lesson', 'Lesson'),
                    #('lesson_team', 'Lesson/Team'),
                    ('team', 'Team'), ('team_new', 'Team (Allow New Teams)'),
                ],
                'value': 'None',
                'help_text': u'Enrolling granularity',
            },
            'password': {
                'help_text': u'Password for enrolling. If empty and enroll is not None, all students can enroll.',
            },
            '_members': {
                'help_text': u'These are only DIRECT members of this event. '
                    'You might want to add users to lessons and/or teams instead.',
            },
        },
        '__field_validator_types__': {'_url': PlainText},
        '__field_validators__': {
            'enroll': twc.validation.OneOfValidator(values=['event', 'lesson', 'lesson_team', 'team', 'team_new']),
        },
        '__possible_field_names__': ['user_name', '_name', 'name', 'title'],
        '__require_fields__': ['type', '_url'],
    }


class LessonsCrudController(FilterCrudRestController):
    '''CrudController for Lessons'''

    model = Lesson

    __table_options__ = {
        '__omit_fields__': [
            'id', 'event_id', 'event', '_url',
            '_students', '_tutor', '_tutor_id',
        ],
        '__field_order__': [
            'lesson_id', 'name',
            'tutors', 'teams', '_members',
        ],
        '__search_fields__': [
            'id', 'lesson_id', 'name',
            ('teams', 'team_id'), ('_members', 'member_id'),
        ],
        # '__headers__': {'_students': 'Students'},
        '__xml_fields__': ['tutors', 'teams', '_members'],
        'tutors': lambda filler, obj:
            ', '.join(link_to(tutor.display_name, '../tutors/%d/edit' % tutor.id)
                for tutor in set(obj.tutors)),
        'teams': lambda filler, obj:
            ', '.join(link_to(team.name, '../teams/%d/edit' % team.id)
                for team in obj.teams),
        '_members': lambda filler, obj:
            ', '.join(link_to(student.display_name, '../students/%d/edit' % student.id)
                for student in obj._members),
        '__base_widget_args__': {'sortList': [[1, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': ['id', '_url', '_students', '_tutor', '_tutor_id'],
        '__hide_fields__': ['event'],  # If the field is omitted, it does not get validated!
        '__field_order__': ['id', 'lesson_id', 'name', 'tutors', 'teams', '_members'],
        '__field_widget_args__': {
            'lesson_id': {
                'label': u'Lesson Id',
                'help_text': u'This id will be part of the url and has to be unique for the parent event',
            },
            '_members': {
                'help_text': u'These are only DIRECT members of this lesson.'
                    'You might want to add users to teams instead.',
            },
        },
        '__possible_field_names__': ['user_name', '_name', 'name', 'title'],
    }
