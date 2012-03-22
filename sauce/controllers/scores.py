# -*- coding: utf-8 -*-
"""Scores controller module"""

import logging

# turbogears imports
from tg import expose, request
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Submission, Assignment, Event

log = logging.getLogger(__name__)

reward = -1
penalty = 20

class ScoresController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    def __init__(self, event_id=None):
        if event_id:
            self.event_id = event_id
            self.event = DBSession.query(Event).filter_by(id=self.event_id).one()
        else:
            self.event = None
    
    @expose('sauce.templates.scores')
    def index(self):
        
        assignment_query = DBSession.query(Assignment)
        submission_query = DBSession.query(Submission).join(Assignment)
        if self.event_id:
            assignment_query = assignment_query.filter(Assignment.event_id == self.event_id)
            submission_query = submission_query.filter(Assignment.event_id == self.event_id)
        
        teams = [team for team in self.event.teams]
        for team in teams:
            team.score = 0
            team.count = 0
        
        for assignment in assignment_query.all():
            assignment.done = False
            for submission in (submission for submission in assignment.submissions if submission.complete):
                assert submission.team in teams
                if not assignment.done:
                    if submission.testrun.result:
                        submission.team.score += reward
                        submission.team.count += 1
                        assignment.done = True
                    else:
                        submission.team.score += penalty
        
        return dict(page='scores', event=self.event, teams=teams)

