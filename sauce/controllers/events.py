# -*- coding: utf-8 -*-
"""Events controller module"""

import logging
from datetime import datetime

# turbogears imports
from tg import expose, abort
#from tg import redirect, validate, flash
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, Event
from sauce.controllers.assignments import AssignmentsController
from sauce.controllers.submissions import SubmissionsController
from sauce.controllers.scores import ScoresController
from sauce.controllers.sheets import SheetsController

log = logging.getLogger(__name__)

class EventController(object):
    
    def __init__(self, event):
        self.event = event
        self.assignments = AssignmentsController(event_id=self.event.id)
        self.submissions = SubmissionsController(event_id=self.event.id)
        self.scores = ScoresController(event_id=self.event.id)
        self.sheets = SheetsController(event_id=self.event.id)
    
    @expose('sauce.templates.event')
    def index(self):
        
        
        
        return dict(page='events', event=self.event)

class EventsController(BaseController):
    
    @expose('sauce.templates.events')
    def index(self, page=1):
        
        events = Page(Event.current_events(), page=page, items_per_page=10)
        future_events = Page(Event.future_events(), page=page, items_per_page=10)
        previous_events = Page(Event.previous_events(), page=page, items_per_page=10)
        
        return dict(page='events', events=events, previous_events=previous_events, future_events=future_events)
    
    @expose()
    def _lookup(self, url, *args):
        '''Return EventController for specified url'''
        event = Event.by_url(url)
        controller = EventController(event)
        return controller, args
