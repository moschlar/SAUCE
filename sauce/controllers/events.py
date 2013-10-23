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
from tg import expose, abort, tmpl_context as c, flash, require, redirect, TGController, url, request
from tg.decorators import paginate

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from repoze.what.predicates import not_anonymous, has_permission, Any
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from webob.exc import HTTPForbidden
from sauce.lib.authz import has_teacher, is_public
from sauce.lib.menu import menu
from sauce.model import Event, Lesson, Team
from sauce.controllers.sheets import SheetsController
from sauce.controllers.lessons import LessonsController, SubmissionsController
from sauce.controllers.event_admin import EventAdminController
from sauce.widgets.enroll import PasswordEnrollForm, TeamSelectionForm, LessonSelectionForm

log = logging.getLogger(__name__)


class EventController(TGController):

    def __init__(self, event):
        self.event = event
        self.sheets = SheetsController(event=self.event)
        self.lessons = LessonsController(event=self.event)
        self.admin = EventAdminController(event=self.event)
        self.submissions = SubmissionsController(event=self.event)
        c.event = self.event

        self.allow_only = Any(
            is_public(self.event),
            has_teacher(self.event),
            has_permission('manage'),
            msg=u'This Event is not public'
        )

        c.sub_menu = menu(self.event, True)

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        #c.side_menu = entity_menu(self.event, 'Sheets', self.event.sheets)
        c.sub_menu = menu(self.event)

    @expose('sauce.templates.event')
    def index(self, *args, **kwargs):
        '''Event details page'''
        return dict(page='events', event=self.event)

    @expose('sauce.templates.form')
    @require(not_anonymous(msg=u'Only logged in users can enroll for events'))
    def enroll(self, password=None, lesson=None, team=None, *args, **kwargs):
        '''Event enrolling page'''

        params = {}

        if not self.event.enroll:
            flash('Enroll not allowed', 'error')
            return HTTPForbidden()

        if self.event.password and password != self.event.password:
            if password:
                flash('Wrong password', 'error')
            c.form = PasswordEnrollForm
        else:
            if password:
                params['password'] = password

            if self.event.enroll == 'event':
                flash('Event "%s" selected, which has no effect atm :(' % self.event.name, 'warning')
                redirect(self.event.url)

            if self.event.enroll == 'team' and team:
                team = Team.query.get(int(team))
                if team:
                    team.members.append(request.user)
                    flash('Team "%s" selected' % team.name, 'ok')
                    redirect(self.event.url)
                else:
                    flash('Team does not exist', 'error')

            if self.event.enroll in ('team', 'lesson') and not lesson:
                c.form = LessonSelectionForm(event=self.event, action=url('', params))

            if self.event.enroll == 'lesson' and lesson:
                lesson = Lesson.query.get(int(lesson))
                if lesson:
                    lesson._members.append(request.user)
                    flash('Lesson "%s" selected' % lesson.name, 'ok')
                    redirect(self.event.url)
                else:
                    flash('Lesson does not exist', 'error')

            if self.event.enroll == 'team' and lesson:
                lesson = Lesson.query.get(int(lesson))
                c.form = TeamSelectionForm(lesson=lesson, action=url('', params))

        return dict(page='events', heading=u'Enroll for %s' % self.event.name)


class EventsController(TGController):

    @expose('sauce.templates.events')
    @paginate('events', use_prefix=True, max_items_per_page=65535)
    @paginate('future_events', use_prefix=True, max_items_per_page=65535)
    @paginate('previous_events', use_prefix=True, max_items_per_page=65535)
    def index(self, *args, **kwargs):
        '''Event listing page'''

        events = Event.current_events()
        future_events = Event.future_events()
        previous_events = Event.previous_events()

        return dict(page='events', events=events,
            previous_events=previous_events, future_events=future_events)

    @expose()
    def _lookup(self, url, *args):
        '''Return EventController for specified url'''

        try:
            event = Event.by_url(url)
        except NoResultFound:
            flash('Event %s not found' % url, 'error')
            abort(404)
        except MultipleResultsFound:
            log.error('Database inconsistency: Event %s' % url, exc_info=True)
            flash('An error occurred while accessing Event %s' % url, 'error')
            abort(500)

        controller = EventController(event)
        return controller, args
