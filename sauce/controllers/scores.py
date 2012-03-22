# -*- coding: utf-8 -*-
"""Scores controller module"""

# turbogears imports
from tg import expose, request
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Submission, Assignment, Event

reward = -1
penalty = 20

class ScoresController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    def __init__(self, event_id=None):
        if event_id:
            self.event_id = event_id
            self.event = DBSession.query(Event).filter_by(id=self.event_id).one()
    
    @expose('sauce.templates.scores')
    def index(self):
        
        #if request.student and request.student.events:
        #    event_id = request.student.events[-1].id
        
        submission_query = DBSession.query(Submission).join(Assignment)
        if self.event_id:
            submission_query = submission_query.filter(Assignment.event_id == self.event_id)
        submissions = submission_query.all()
        
        teams = [team for team in self.event.teams]
        
        teams = []
        
        return dict(page='scores', event=self.event, teams=teams)
