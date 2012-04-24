# -*- coding: utf-8 -*-
"""Events controller module

@author: moschlar
"""

import logging
from datetime import datetime

# turbogears imports
from tg import expose, abort, require, tmpl_context as c, validate, redirect, flash, url, request
from tg.controllers import TGController
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from repoze.what.predicates import not_anonymous, has_permission

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.base import BaseController, do_navigation_links
import sauce.model as model
from sauce.model import DBSession, Event, Lesson, Team, Student
#from sauce.controllers.assignments import AssignmentsController
#from sauce.controllers.submissions import SubmissionsController
#from sauce.controllers.scores import ScoresController
from sauce.controllers.sheets import SheetsController
from sauce.controllers.lessons import LessonsController

from sauce.lib.auth import has_teacher
from sauce.lib.helpers import link
from sauce.controllers.event_admin import EventAdminController

log = logging.getLogger(__name__)

class EventController(TGController):
    
    def __init__(self, event):
        
        self.event = event
        self.sheets = SheetsController(event=event)
        self.lessons = LessonsController(event=event)
        self.admin = EventAdminController(event=event)
        
        c.event = event
        c.navigation = do_navigation_links(event)
    
    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with breadcrumbs'''
        c.breadcrumbs = self.event.breadcrumbs

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
        
        return dict(page='events', events=events, previous_events=previous_events, future_events=future_events)
    
    @expose()
    def _lookup(self, url, *args):
        '''Return EventController for specified url'''
        
        try:
            event = Event.by_url(url)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        c.navigation = do_navigation_links(event)
        
        controller = EventController(event)
        return controller, args
