# -*- coding: utf-8 -*-
'''
Created on 12.11.2012

@author: moschlar
'''

import logging

import tw2.tinymce as twt
import tw2.bootstrap.forms as twb
import tw2.jqplugins.chosen.widgets as twjc
from formencode.validators import PlainText
from webhelpers.html.tags import link_to

from sauce.model import Event, Lesson

__all__ = ['EventsCrudController', 'LessonsCrudController']

log = logging.getLogger(__name__)

from sauce.controllers.crc.base import FilterCrudRestController


class EventsCrudController(FilterCrudRestController):

    model = Event

    __table_options__ = {
        '__omit_fields__': ['id', 'description', 'teacher_id', 'password',
                            'assignments', 'lessons', 'sheets', 'news',
                           ],
        '__field_order__': ['type', '_url', 'name', 'public',
                            'start_time', 'end_time', 'teacher', 'tutors'],
        '__search_fields__': ['id', '_url', 'name', 'teacher_id'],
#        '__headers__': {'_url': 'Url'},
        '__xml_fields__': ['teacher', 'tutors'],
        'start_time': lambda filler, obj: obj.start_time.strftime('%c'),
        'end_time': lambda filler, obj: obj.end_time.strftime('%c'),
        'teacher': lambda filler, obj: link_to(obj.teacher.display_name, '../tutors/%d/edit' % obj.teacher.id),
        'tutors': lambda filler, obj: ', '.join(link_to(tutor.display_name, '../tutors/%d/edit' % tutor.id) for tutor in obj.tutors),
        '__base_widget_args__': {'sortList': [[6, 1], [5, 1]]},
        }
    __form_options__ = {
        '__hide_fields__': ['teacher'],
        '__omit_fields__': ['id', 'assignments', 'sheets', 'news', 'lessons', 'password'],
        '__field_order__': ['id', 'type', '_url', 'name', 'description',
                            'public', 'start_time', 'end_time'],
        '__field_widget_types__': {'name': twb.TextField, 'description': twt.TinyMCEWidget,
                                   '_url': twb.TextField,
                                   'type': twjc.ChosenSingleSelectField,
                                  },
        '__field_validator_types__': {'_url': PlainText, },
        '__field_widget_args__': {
                                  'type': dict(options=[('course', 'Course'), ('contest', 'Contest')],
                                      value='course', prompt_text=None, required=True),
                                  'name': {'css_class': 'span4'},
                                  'description': {'css_class': 'span7'},
                                  'start_time': {'date_format': '%d.%m.%Y %H:%M'},
                                  'end_time': {'date_format': '%d.%m.%Y %H:%M'},
                                  '_url': {'help_text': u'Will be part of the url, has to be unique and url-safe'},
                                  'public': {'help_text': u'Make event visible for students', 'default': True},
                                  'password': {'help_text': u'Password for student self-registration. Currently not implemented'},
                                 },
        '__require_fields__': ['_url'],
        }


class LessonsCrudController(FilterCrudRestController):

    model = Lesson

    __table_options__ = {
        '__omit_fields__': ['id', 'event_id', 'event', '_url', '_members'],
        '__field_order__': ['lesson_id', 'name', 'tutor_id',
                            'tutor', 'teams', '_students'],
        '__search_fields__': ['id', 'lesson_id', 'name', 'tutor_id',
            ('teams', 'team_id'), ('_students', 'student_id')],
#        '__headers__': {'_students': 'Students'},
        '__xml_fields__': ['tutor', 'teams', '_students'],
        'tutor': lambda filler, obj: link_to(obj.teacher.display_name, '%s/teachers/%d/edit'
            % (filler.path_prefix, obj.teacher.id)),
        'teams': lambda filler, obj: ', '.join(link_to(team.name, '%s/teams/%d/edit'
            % (filler.path_prefix, team.id)) for team in obj.teams),
        '_students': lambda filler, obj: ', '.join(link_to(student.display_name, '%s/students/%d/edit'
            % (filler.path_prefix, student.id)) for student in obj._members),
        '__base_widget_args__': {'sortList': [[1, 0]]},
        }
    __form_options__ = {
        '__omit_fields__': ['id', '_url', 'teams', '_students', '_members'],
        '__hide_fields__': ['event'],  # If the field is omitted, it does not get validated!
        '__field_order__': ['id', 'lesson_id', 'name', 'tutor'],
        '__field_widget_types__': {'name': twb.TextField},
        '__field_widget_args__': {
                                  'lesson_id': {'label': u'Lesson Id', 'help_text': u'This id will be part of the url and has to be unique for the parent event'},
                                  'name': {'css_class': 'span7'},
                                 },
        }
