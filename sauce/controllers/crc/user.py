# -*- coding: utf-8 -*-
'''
Created on 12.11.2012

@author: moschlar
'''

import logging

from tg import flash

#from tw2.forms import TextField, SingleSelectField, Label, TextArea, CheckBox
#from tw2.tinymce import TinyMCEWidget
#import tw2.core as twc
import tw2.tinymce as twt
import tw2.bootstrap.forms as twb
from webhelpers.html.tags import link_to

from sauce.model import Team, User

from sauce.controllers.crc.base import FilteredCrudRestController

__all__ = ['TeamsCrudController', 'StudentsCrudController', 'TutorsCrudController']

log = logging.getLogger(__name__)


def _email_team(filler, obj):
    return u'<a href="mailto:%s?subject=%%5BSAUCE%%5D" class="btn btn-mini"'\
        'onclick="return confirm(\'This will send an eMail to %d people. '\
        'Are you sure?\')">'\
        '<i class="icon-envelope"></i>&nbsp;eMail</a>' % (','.join(s.email_address for s in obj.students), len(obj.students))


class TeamsCrudController(FilteredCrudRestController):

    model = Team

    __table_options__ = {
        #'__omit_fields__': ['lesson_id'],
        '__field_order__': ['id', 'name', 'lesson_id', 'lesson', 'members', 'email'],
        '__search_fields__': ['id', 'lesson_id', 'name'],
        '__xml_fields__': ['lesson', 'members', 'email'],
        'lesson': lambda filler, obj: link_to(obj.lesson.name, '../lessons/%d/edit' % obj.lesson.id),
        'members': lambda filler, obj: ', '.join(link_to(student.display_name, '../students/%d/edit' % student.id) for student in obj.members),
        'email': _email_team,
        '__base_widget_args__': {'sortList': [[3, 0], [1, 0]]},
        }
    __form_options__ = {
        '__omit_fields__': ['id'],
        '__field_order__': ['id', 'name', 'lesson', 'members'],
        '__field_widget_types__': {'name': twb.TextField},
        '__field_widget_args__': {'members': {'size': 10, 'css_class': 'span7'}},
        }


#--------------------------------------------------------------------------------


def set_password(user):
    '''Sets the password for user to a new autogenerated password and displays it via flash'''
    password = user.generate_password()
    flash('Password for User %s set to: %s' % (user.user_name, password), 'info')
    return password


def _new_password(filler, obj):
    return u'<a href="%d/password" class="btn btn-mini"'\
        'onclick="return confirm(\'This will generate a new, randomized '\
        'password for the User %s and show it to you. Are you sure?\')">'\
        '<i class="icon-random"></i> New password</a>' % (obj.id, obj.display_name)


def _email_address(filler, obj):
    return u'<a href="mailto:%s?subject=%%5BSAUCE%%5D" style="white-space: pre;" class="btn btn-mini">'\
        '<i class="icon-envelope"></i>&nbsp;'\
        '%s</a>' % (obj.email_address, obj.email_address)


class StudentsCrudController(FilteredCrudRestController):

    model = User
    menu_item = u'Student'

    __table_options__ = {
        '__omit_fields__': [
            'type', 'groups',
            'password', '_password',
            'last_name', 'first_name',
            'submissions',
            'tutored_lessons'
            ],
        '__field_order__': [
            'id', 'user_name',
            'display_name', 'email_address',
            'teams', '_lessons',
            'created', 'new_password'],
        '__search_fields__': [
            'id', 'user_name', 'email_address',
            ('teams', 'team_id'), ('lessons', 'lesson_id')],
#        '__headers__': {
#            'new_password': u'Password',
#            '_lessons': u'Lessons'},
        '__xml_fields__': ['_lessons', 'teams', 'email_address', 'new_password'],
        'created': lambda filler, obj: obj.created.strftime('%c'),
        'display_name': lambda filler, obj: obj.display_name,
        'new_password': _new_password,
        'email_address': _email_address,
        'teams': lambda filler, obj: ', '.join(link_to(team.name, '../teams/%d/edit' % team.id) for team in obj.teams),
        '_lessons': lambda filler, obj: ', '.join(link_to(lesson.name, '../lessons/%d/edit' % lesson.id) for lesson in obj._lessons),
        '__base_widget_args__': {
            'headers': {8: {'sorter': False}},
            'sortList': [[6, 0], [5, 0], [3, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': [
            'id', 'type', 'groups',
            'created', 'display_name',
            'password', '_password',
            'submissions', 'tutored_lessons'],
        '__field_order__': [
            'id', 'user_name', 'last_name', 'first_name',
            'email_address',
            'teams', '_lessons',
        ],
        '__field_widget_types__': {
            'user_name': twb.TextField, 'email_address': twb.TextField,
            'last_name': twb.TextField, 'first_name': twb.TextField,
        },
        '__field_widget_args__': {
            'last_name': dict(css_class='span4'), 'first_name': dict(css_class='span4'),
            'email_address': dict(css_class='span4'),
            'user_name': {'help_text': u'Desired user name for login', 'css_class': 'span4'},
            'teams': {'help_text': u'These are the teams this student belongs to',
                      'size': 10, 'css_class': 'span7'},
            '_lessons': {'help_text': u'These are the lessons this students directly belongs to '
                         '(If he belongs to a team that is already in a lesson, this can be left empty)',
                      'size': 5, 'css_class': 'span7'},
        #TODO: Make this working somehow
        '__unique__fields__': ['email_address'],
        },
    }
    __setters__ = {
        'password': ('password', set_password),
    }


class TutorsCrudController(FilteredCrudRestController):

    model = User
    menu_item = u'Tutor'

    __table_options__ = {
        '__omit_fields__': [
            'type', 'groups',
            'password', '_password',
            'last_name', 'first_name',
            'submissions',
            '_lessons', 'teams',
            ],
        '__field_order__': [
            'id', 'user_name',
            'display_name', 'email_address',
            'tutored_lessons',
            'created', 'new_password'],
        '__search_fields__': [
            'id', 'user_name', 'email_address',
            ('tutored_lessons', 'lesson_id')],
#        '__headers__': {
#            'new_password': u'Password',
#            'tutored_lessons': u'Lessons'},
        '__xml_fields__': ['tutored_lessons', 'email_address', 'new_password'],
        'created': lambda filler, obj: obj.created.strftime('%c'),
        'display_name': lambda filler, obj: obj.display_name,
        'new_password': _new_password,
        'email_address': _email_address,
        'tutored_lessons': lambda filler, obj: ', '.join(link_to(lesson.name, '../lessons/%d/edit' % lesson.id) for lesson in obj.tutored_lessons),
        '__base_widget_args__': {
            'headers': {7: {'sorter': False}},
            'sortList': [[5, 0], [3, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': [
            'id', 'type', 'groups',
            'created', 'display_name',
            'password', '_password',
            'submissions',
            '_lessons', 'teams'
        ],
        '__field_order__': [
            'id', 'user_name', 'last_name', 'first_name',
            'email_address',
            'tutored_lessons',
        ],
        '__field_widget_types__': {
            'user_name': twb.TextField, 'email_address': twb.TextField,
            'last_name': twb.TextField, 'first_name': twb.TextField,
        },
        '__field_widget_args__': {
            'last_name': dict(css_class='span4'), 'first_name': dict(css_class='span4'),
            'email_address': dict(css_class='span4'),
            'user_name': {'help_text': u'Desired user name for login', 'css_class': 'span4'},
            'tutored_lessons': {'help_text': u'These are the lessons this tutor teaches',
                'size': 10, 'css_class': 'span7'},
        #TODO: Make this working somehow
        '__unique__fields__': ['email_address'],
        },
    }
    __setters__ = {
        'password': ('password', set_password),
    }


class TeachersCrudController(TutorsCrudController):

    menu_item = u'Teacher'
