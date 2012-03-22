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

log = logging.getLogger(__name__)

class EventController(object):
    
    def __init__(self, event_id):
        self.event_id = event_id
        self.assignments = AssignmentsController(event_id=self.event_id)
        self.submissions = SubmissionsController(event_id=self.event_id)
        self.scores = ScoresController(event_id=self.event_id)
    
    @expose('sauce.templates.event')
    def index(self):
        
        try:
            event = DBSession.query(Event).filter_by(id=self.event_id).one()
        except NoResultFound:
            abort(404, 'Event %d not found' % self.event_id, 
                  comment='Event %d not found' % self.event_id)
        
        return dict(page='events', event=event)

class EventsController(BaseController):
    
    @expose('sauce.templates.events')
    def index(self, page=1):
        
        event_query = DBSession.query(Event)
        events = Page(event_query.filter(Event.end_time > datetime.now()), page=page, items_per_page=10)
        past_events = Page(event_query.filter(Event.end_time < datetime.now()), page=page, items_per_page=10)
        
        return dict(page='events', events=events, past_events=past_events)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return EventController for specified id'''
        
        event_id = int(id)
        controller = EventController(event_id)
        return controller, args
