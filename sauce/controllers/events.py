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
from tg import expose, abort, tmpl_context as c, flash, TGController
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from repoze.what.predicates import has_permission, Any
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.auth import has_teacher, is_public
from sauce.lib.menu import menu
from sauce.model import Event
from sauce.controllers.sheets import SheetsController
from sauce.controllers.lessons import LessonsController
from sauce.controllers.event_admin import EventAdminController

log = logging.getLogger(__name__)


class EventController(TGController):

    def __init__(self, event):
        self.event = event
        self.sheets = SheetsController(event=self.event)
        self.lessons = LessonsController(event=self.event)
        self.admin = EventAdminController(event=self.event)
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
    def index(self):
        '''Event details page'''
        return dict(page='events', event=self.event)

#    #@expose()
#    @require(not_anonymous(msg=u'Only logged in users can enroll for events'))
#    def enroll(self):
#        '''Event enrolling page'''
#
#        password = self.event.password
#
#        return dict(page='events', enroll=True)


class EventsController(TGController):

    @expose('sauce.templates.events')
    def index(self, page=1):
        '''Event listing page'''

        events = Page(Event.current_events(), page=page, items_per_page=10)
        future_events = Page(Event.future_events(), page=page, items_per_page=10)
        previous_events = Page(Event.previous_events(), page=page, items_per_page=10)

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
