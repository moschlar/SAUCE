# -*- coding: utf-8 -*-
"""Events controller module"""

import logging

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

log = logging.getLogger(__name__)

class EventController(object):
    
    def __init__(self, event_id):
        self.event_id = event_id
    
    @expose('sauce.templates.event')
    def index(self):
        
        try:
            event = DBSession.query(Event).filter_by(id=self.event_id).one()
        except NoResultFound:
            abort(404, 'Event %d not found' % self.event_id, comment='Event %d not found' % self.event_id)
        
        return dict(page='events', event=event)

class EventsController(BaseController):
    
    @expose('sauce.templates.events')
    def index(self, page=1):
        
        event_query = DBSession.query(Event)
        events = Page(event_query, page=page, items_per_page=5)
        
        return dict(page='events', events=events)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return EventController for specified id'''
        
        id = int(id)
        event = EventController(id)
        return event, args
