# -*- coding: utf-8 -*-
"""Scores controller module

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
from tg import expose, request, TGController

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Submission, Assignment, Event, Team
#from sauce.model.user import team_to_event

log = logging.getLogger(__name__)

reward = -1
penalty = 20


class ScoresController(TGController):

    def __init__(self, event=None):
        self.event = event
        raise Exception('This class is not up-to-date with the application and can not be used.')

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
            for submission in (submission for submission in assignment.submissions if submission.result is not None):
                try:
                    assert submission.team in teams
                    if not assignment.done.get(submission.team.id):
                        if submission.testrun.result:
                            submission.team.score += int((submission.testrun.date - assignment.start_time).seconds / 60)
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
