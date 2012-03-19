# -*- coding: utf-8 -*-
"""Submission controller module"""

import logging

# turbogears imports
from tg import expose, request
#from tg import redirect, validate, flash

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _
from repoze.what import authorize
from repoze.what.predicates import has_permission

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Submission, TestRun
import transaction

from sauce.lib.runner import Runner
from sauce.lib.auth import has_student

from time import time
from collections import namedtuple

results = namedtuple('results', ('succeeded', 'failed', 'total', 'result'))

log = logging.getLogger(__name__)

def evaluateTestruns(testruns):
    succeeded = 0
    failed = 0
    for testrun in testruns:
        if testrun:
            succeeded += 1
        else:
            failed += 1
    return results(succeeded, failed, succeeded+failed, (failed == 0) and (succeeded + failed > 0))

class SubmissionController(BaseController):
    
    def __init__(self, submission_id):
        self.submission_id = submission_id
        self.allow_only = has_student(type=Submission, id=submission_id, msg='You may only view your own submissions')
    
    @expose('sauce.templates.submission')
    def index(self):
        submission = DBSession.query(Submission).filter(Submission.id == self.submission_id).one()
        return dict(page='submissions', submission=submission)
    
    @expose('sauce.templates.test')
    def test(self):
        submission = DBSession.query(Submission).filter(Submission.id == self.submission_id).one()
        
        with Runner(submission) as r:
            start = time()
            compilation = r.compile()
            end = time()
            log.info('Submission %d compilation time: %f' % (submission.id, end - start))
            if not compilation or compilation.returncode == 0:
                start = time()
                testruns = [testrun for testrun in r.test()]
                end = time()
                log.info('Submission %d run time: %f' % (submission.id, end - start))
                results = evaluateTestruns(testruns)
                testrun = TestRun(submission=submission, succeeded=results.succeeded, 
                                  failed=results.failed, result=results.result, runtime=end - start)
                DBSession.add(testrun)
                transaction.commit()
            else:
                testruns = []
                results = ()
        submission = DBSession.query(Submission).filter(Submission.id == self.submission_id).one()
        return dict(page='submissions', submission=submission, compilation=compilation, 
                    testruns=testruns, results=results)

class SubmissionsController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous(msg='You have to be logged in to view submissions')
    
    @expose('sauce.templates.submissions')
    def index(self, page=1):
        
        submission_query = DBSession.query(Submission).filter(Submission.student == request.student)
        
        submissions = Page(submission_query, page=page, items_per_page=10)
        
        return dict(page='submissions', submissions=submissions)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return SubmissionController for specified id'''
        id=int(id)
        submission = SubmissionController(id)
        return submission, args
    
