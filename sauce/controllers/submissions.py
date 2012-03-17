# -*- coding: utf-8 -*-
"""Submission controller module"""

# turbogears imports
from tg import expose
#from tg import redirect, validate, flash

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Submission
import transaction

from sauce.lib.runner import Runner
from sauce.model.test import TestRun

from collections import namedtuple

results = namedtuple('results', ('succeeded', 'failed', 'result'))

def evaluateTestruns(testruns):
    succeeded = 0
    failed = 0
    for testrun in testruns:
        if testrun.returncode == 0:
            succeeded += 1
        else:
            failed += 1
    return results(succeeded, failed, (failed == 0) and (succeeded + failed > 0))

class SubmissionController(object):
    
    def __init__(self, submission_id):
        self.submission_id = submission_id
    
    @expose('sauce.templates.submission')
    def index(self):
        submission = DBSession.query(Submission).filter(Submission.id == self.submission_id).one()
        return dict(page='submissions', submission=submission)
    
    @expose('sauce.templates.test')
    def test(self):
        submission = DBSession.query(Submission).filter(Submission.id == self.submission_id).one()
        
        with Runner(submission) as r:
            compilation = r.compile()
            
            if not compilation or compilation.returncode == 0:
                testruns = [testrun for testrun in r.test()]
                results = evaluateTestruns(testruns)
                testrun = TestRun(submission, succeeded=results.succeeded, failed=results.failed, result=results.result)
                DBSession.add(testrun)
                transaction.commit()
            else:
                testruns = []
                results = ()
        submission = DBSession.query(Submission).filter(Submission.id == self.submission_id).one()
        return dict(page='submissions', submission=submission, compilation=compilation, testruns=testruns, results=results)

class SubmissionsController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.submissions')
    def index(self, page=1):
        
        submission_query = DBSession.query(Submission)
        
        submissions = Page(submission_query, page=page, items_per_page=10)
        
        return dict(page='submissions', submissions=submissions)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return SubmissionController for specified id'''
        id=int(id)
        submission = SubmissionController(id)
        print id, args
        return submission, args
    
