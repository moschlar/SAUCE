# -*- coding: utf-8 -*-
"""Scores controller module"""

# turbogears imports
from tg import expose
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Submission, Assignment

reward = -1
penalty = 1

class ScoresController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.scores')
    def index(self, event_id=1):
        submissions = DBSession.query(Submission).join(Assignment).filter(Assignment.event_id == event_id).all()
        students = []
        for submission in submissions:
            if not submission.student in students:
                submission.student.score=0
                students.append(submission.student)
            for testrun in submission.testruns:
                if testrun.result:
                    submission.student.score += reward
                else:
                    submission.student.score += penalty
        students = sorted(students, key=lambda student: student.score)
        return dict(page='scores', students=students)