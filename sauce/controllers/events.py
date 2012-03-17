# -*- coding: utf-8 -*-
"""Sample controller module"""

# turbogears imports
from tg import expose
#from tg import redirect, validate, flash
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Event

class EventController(object):
    
    def __init__(self, event_id):
        self.event_id = event_id
    
    @expose('sauce.templates.event')
    def index(self):
        event = DBSession.query(Event).filter_by(id=self.event_id).one()
        return dict(page='events', event=event)

class EventsController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.events')
    def index(self, page=1):
        event_query = DBSession.query(Event)
        
        events = Page(event_query, page=page, items_per_page=1)
        
        return dict(page='events', events=events)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return EventController for the specified id'''
        id = int(id)
        event = EventController(id)
        return event, args