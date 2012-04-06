# -*- coding: utf-8 -*-
"""Scores controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, request
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Submission, Assignment, Event, Team
#from sauce.model.person import team_to_event

log = logging.getLogger(__name__)

reward = -1
penalty = 20

class ScoresController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    def __init__(self, event=None):
        self.event = event
    
    @expose('sauce.templates.scores')
    def index(self):
        
        assignment_query = DBSession.query(Assignment)
        submission_query = DBSession.query(Submission).join(Assignment)
        team_query = DBSession.query(Team)
        if self.event_id:
            assignment_query = assignment_query.filter(Assignment.event_id == self.event_id)
            submission_query = submission_query.filter(Assignment.event_id == self.event_id)
            #team_query = team_query.join(team_to_event).filter_by(event_id=self.event_id)
        
        teams = team_query.all()
        for team in teams:
            team.score = 0
            team.count = 0
            team.assignments = []
        
        for assignment in assignment_query.all():
            assignment.done = {}
            assignment.solution = {}
            for submission in (submission for submission in assignment.submissions if submission.complete):
                try:
                    assert submission.team in teams
                    if not assignment.done.get(submission.team.id):
                        if submission.testrun.result:
                            submission.team.score += int((submission.testrun.date - assignment.start_time).seconds/60)
                            submission.team.count += 1
                            assignment.done[submission.team.id] = True
                            assignment.solution[submission.team.id] = submission
                            submission.team.assignments.append(assignment)
                        else:
                            submission.team.score += penalty
                except Exception as e:
                    log.warn('Error in submission %d: %s' % (submission.id, e))
        
        teams = sorted(sorted(teams, key=lambda team: team.score), key=lambda team: team.count, reverse=True)
        
        return dict(page='scores', event=self.event, teams=teams)

