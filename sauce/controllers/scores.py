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
from sauce.model import DBSession, metadata, Submission, Assignment

log = logging.getLogger(__name__)

reward = -1
penalty = 20

class ScoresController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.scores')
    def index(self, event_id=3):
        
        if request.student and request.student.events:
            event_id = request.student.events[-1].id
        
        submissions = DBSession.query(Submission).join(Assignment).filter(Assignment.event_id == event_id).all()
        
        students = {}
        assignments = {}
        
        for submission in submissions:
            if not students.get(submission.student.id):
                students[submission.student.id] = dict(score=0, count=0, team_id=submission.student.team.id, 
                                                       team_name=submission.student.team.name, name=submission.student.name)
            
            #students[submission.student.id]
            
            if submission.testrun:
                if submission.testrun.result:
                    if not assignments.get(submission.assignment.id):
                        assignments[submission.assignment.id] = True
                        students[submission.student.id]['count'] += 1
                        students[submission.student.id]['score'] += int((submission.testrun.date - submission.assignment.start_time).seconds/60)
                else:
                    students[submission.student.id]['score'] += penalty
        
        teams = {}
        
        for id in students:
            if students[id]['team_id']:
                if not teams.get(students[id]['team_id']):
                    teams[students[id]['team_id']] = dict(score=0, count=0, name=students[id]['team_name'])
                teams[students[id]['team_id']]['score'] += students[id]['score']
                teams[students[id]['team_id']]['count'] += students[id]['count']
        
        log.info(students)
        log.info(teams)
        
        # Sort students
        students = sorted(sorted(students.values(), key=lambda student: student['score']), key=lambda student: student['count'], reverse=True)
        
        # Sort teams
        teams = sorted(sorted(teams.values(), key=lambda team: team['score']), key=lambda team: team['count'], reverse=True)
        
        log.info(students)
        log.info(teams)
        
        return dict(page='scores', students=students, teams=teams)
