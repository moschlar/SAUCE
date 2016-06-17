# -*- coding: utf-8 -*-
"""Events controller module

@author: moschlar
"""
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

# turbogears imports
from tg import expose, abort, tmpl_context as c, flash, require, redirect, url, request
from tg.decorators import before_call

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from repoze.what.predicates import not_anonymous, has_permission

# project specific imports
from sauce.controllers.crc.event import EventsCrudController
from sauce.lib.misc import merge

import tw2.bootstrap.forms as twb
from sauce.lib.mail import sendmail

log = logging.getLogger(__name__)


def enable_event(event):
    sendmail(u'[SAUCE] Event request granted', u'''
Your Request for the Event "%s" in SAUCE has been granted.
You can now access the event at %s.
''' % (event.name, url(event.url, qualified=True)),
        to_addrs=event.teacher.email_address, cc_managers=True)
    return True


class EventRequestController(EventsCrudController):

    allow_only = not_anonymous()

    __table_options__ = {
        '__omit_fields__!': [
            'id', 'description', 'password',
            '_teacher', '_teacher_id',
            '_assignments', 'lessons', 'sheets', 'news',
            'tutors', '_members', 'lti',
            'enabled',
        ],
        '__field_order__!': [
            'type', '_url', 'name', 'public',
            'start_time', 'end_time',
            'teachers', 'enroll',
        ],
        #'__search_fields__!': None,
        'teachers!': lambda filler, obj:
            ', '.join(teacher.display_name for teacher in set(obj.teachers)),
        'tutors!': lambda filler, obj:
            ', '.join(tutor.display_name for tutor in obj.tutors),
        '_members!': lambda filler, obj:
            ', '.join(student.display_name for student in obj._members),
    }

    __form_options__ = {
        '__omit_fields__!': [
            'id', '_assignments', 'sheets', 'news', 'lessons',
            '_teacher', '_teacher_id', 'enabled',
            'teachers', '_members',
            'lti',
        ],
        '__field_order__!': [
            'id', 'type',
            '_url', 'name', 'description',
            'public', 'enroll', 'password',
            'start_time', 'end_time',
        ],
        '__field_widget_types__': {
            'type': twb.RadioButtonTable,
        },
        '__field_widget_args__': {
            'type': {
                'name': 'type', 'id': 'type',
                'cols': 2,
                'options': [
                    ('course', 'Course'), ('contest', 'Contest'),
                ],
                'value': 'course',
#                 'help_text': u'Enrolling granularity',
            },
        },
    }

    __setters__ = {
        'enable': ('enabled', enable_event),
    }

    def __init__(self, *args, **kwargs):
        '''Merge __form_options__ from parent class and child class'''
        self.__table_options__ = merge(EventsCrudController.__table_options__, self.__table_options__)
        self.__form_options__ = merge(EventsCrudController.__form_options__, self.__form_options__)
#         kwargs['inject'] = dict(teacher=request.user)
        kwargs['query_modifier'] = lambda qry: qry.filter_by(enabled=False)
        kwargs['show_menu'] = False
        super(EventRequestController, self).__init__(*args, **kwargs)

    def _actions(self, obj):
        actions = []
        primary_fields = self.table_filler.__provider__.get_primary_fields(self.table_filler.__entity__)
        pklist = u'/'.join(map(lambda x: unicode(getattr(obj, x)), primary_fields))

        try:
            actions.append(
                u'<a href="%s/enable" class="btn btn-mini btn-success" title="Enable">'
                u'  <i class="icon-ok icon-white"></i>'
                u'</a>' % (pklist))
        except:
            pass
        if self.allow_edit:
            try:
                actions.append(
                    u'<a href="%s/edit" class="btn btn-mini" title="Edit">'
                    u'  <i class="icon-pencil"></i>'
                    u'</a>' % (pklist))
            except:
                pass
        if self.allow_delete:
            actions.append(
                u'<a class="btn btn-mini btn-danger" href="./%d/delete" title="Delete">'
                u'  <i class="icon-remove icon-white"></i>'
                u'</a>' % (obj.id))
        return actions

    @classmethod
    def before_call_get_all(cls, remainder, params):
        self = request.controller_state.controller
        if isinstance(self, cls):
            if not has_permission('manage'):
                return redirect('/events/request/new')

    @expose(inherit=True)
    @require(has_permission('manage'))
    def edit(self, *args, **kw):
        return super(EventRequestController, self).edit(*args, **kw)

    @expose(inherit=True)
    @require(has_permission('manage'))
    def put(self, *args, **kw):
        return super(EventRequestController, self).put(*args, **kw)

    @expose(inherit=True)
    def post(self, *args, **kw):
        # Inject
        kw['teacher'] = request.user
        # Force CrudController.post to return a dict
        ''':type request: tg.request_local.Request'''
        request._response_type = 'application/json'
        result = super(EventRequestController, self).post(*args, **kw)
        value = result['value']
        sendmail(u'[SAUCE] Event requested', u'''
A new Event has been requested in SAUCE.
Review the request at %s.
''' % url('/events/request', qualified=True), cc_managers=True)
        flash('Event "%s" successfully requested. Now awaiting administrator approval.' % (value.name), 'ok')
        return redirect('/')

# Register hook for get_all
before_call(EventRequestController.before_call_get_all)(EventRequestController.get_all)
