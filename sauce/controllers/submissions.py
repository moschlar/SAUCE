# -*- coding: utf-8 -*-
"""Submissionn controller module"""

import logging
from time import time

from collections import namedtuple

# turbogears imports
from tg import expose, request, redirect, url, flash, session, tmpl_context as c
#from tg import redirect, validate, flash
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
from repoze.what import predicates, authorize

from sqlalchemy.orm import joinedload #, joinedload_all, subqueryload, immediateload
from sqlalchemy.orm.exc import NoResultFound
import transaction

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession as Session, Assignment, Submission, Language, TestRun

from sauce.lib.runner import Runner

from sauce.widgets.submission import submission_form
from sauce.lib.auth import has_student

log = logging.getLogger(__name__)
results = namedtuple('results', ('result', 'ok', 'fail', 'total'))

class SubmissionController(BaseController):
    
    allow_only = authorize.not_anonymous()
    
    def __init__(self, assignment_id=None, submission_id=None):
        
        if bool(assignment_id) == (submission_id):
            raise Exception('Both constructor values set, that should never happen')
        
        self.submission_id = None
        
        if assignment_id:
            #self.assignment_id = assignment_id
            self.assignment = Session.query(Assignment).filter_by(id=assignment_id).one()
            #self.submission = Submission(assignment=self.assignment)
            self.submission = Submission()
        
        if submission_id:
            #self.submission_id = submission_id
            self.submission = Session.query(Submission).filter_by(id=submission_id).one()
            
            self.assignment = self.submission.assignment
            #self.assignment_id = self.assignment.id
            
            self.allow_only = has_student(type=Submission, id=submission_id, 
                                      msg='You may only view your own submissions')
    
    def parse_kwargs(self, kwargs):
        
        # Get language from kwargs
        try:
            language_id = int(kwargs['language_id'])
        except KeyError:
            raise Exception('Could not get language_id')
            #redirect(url(request.environ['PATH_INFO']))
        except ValueError:
            raise Exception('Could not parse language_id')
            #redirect(url(request.environ['PATH_INFO']))
        else:
            language = Session.query(Language).filter_by(id=language_id).one()
        
        #log.debug('%s %s' % (self.assignment in Session, language in Session))
        #log.debug('language: %s, allowed_languages: %s' % (repr(language), self.assignment.allowed_languages))    
        
        if language not in self.assignment.allowed_languages:
            raise Exception('The Language %s is not allowed for this assignment' % (language))
            #redirect(url(request.environ['PATH_INFO']))
        
        source = ''
        try:
            source = kwargs['source']
            filename = kwargs['filename'] or '%d_%d.%s' % (request.student.id, self.assignment.id, language.extension_src)
        except:
            pass
        
        try:
            source = kwargs['source_file'].value
            filename = kwargs['source_file'].filename
        except:
            pass
        
        if source.strip() == '':
            raise Exception('Source code is empty, not submitting')
            #redirect(url(request.environ['PATH_INFO']))
        
        return (language, source, filename)
    
    def evalTests(self, tests):
        ok, fail = 0, 0
        for test in tests:
            if test:
                ok += 1
            else:
                fail += 1
        return results(fail == 0 and (ok+fail) > 0, ok, fail, ok+fail)
    
    @expose('sauce.templates.submission')
    def index(self, **kwargs):
        
        # Some initialization
        c.form = submission_form
        c.options = dict()
        c.child_args = dict()
        compilation = None
        testruns = []
        submit = None
        
        #log.debug(kwargs)
        
        if request.environ['REQUEST_METHOD'] == 'POST':
            
            test = kwargs.get('buttons.test')
            submit = kwargs.get('buttons.submit')
            reset = kwargs.get('buttons.reset')
            
            if reset:
                Session.delete(self.submission)
                flash('Resetted', 'ok')
            else:
                try:
                    (language, source, filename) = self.parse_kwargs(kwargs)
                except Exception as e:
                    flash(str(e), 'error')
                else:
                    self.submission.assignment = self.assignment
                    self.submission.student = request.student
                    self.submission.language = language
                    self.submission.source = source
                    self.submission.filename = filename
                    
                    Session.add(self.submission)
                    transaction.commit()
                    self.submission = Session.merge(self.submission)
                    
        if self.submission.source and not self.submission.complete:
            with Runner(self.submission) as r:
                start = time()
                compilation = r.compile()
                end = time()
                compilation_time = end-start
                #log.debug(compilation)
                
                if not compilation or compilation.returncode == 0:
                    start = time()
                    testruns = [testrun for testrun in r.test_visible()]
                    end = time()
                    run_time = end-start
                    #log.debug(testruns)
                    #flash()
                    
                    if [testrun for testrun in testruns if not testrun.result]:
                        flash('Test run did not run successfully, you may not submit', 'error')
                    else:
                        
                        if submit:
                            self.submission.complete = True
                            
                            start = time()
                            tests = [test for test in r.test()]
                            end = time()
                            test_time = end-start
                            
                            testresults = self.evalTests(tests)
                            #log.debug('%f %s %s %s %s' % (test_time, testresults.result, testresults.ok, 
                            #                           testresults.fail, testresults.total))
                            
                            self.submission.result = testresults.result
                            
                            flash('Test result: %s' % testresults.result, 'info')
                            if testresults.result:
                                flash('All tests completed. Runtime: %f' % test_time, 'ok')
                            else:
                                flash('Tests failed. Runtime: %f' % test_time, 'error')
                            
                            self.submission.testrun = TestRun(runtime=test_time, result=testresults.result,
                                                              succeeded=testresults.ok, failed=testresults.fail)
                            
                            transaction.commit()
                            self.submission = Session.merge(self.submission)
                            redirect(url('/submissions/%d' % self.submission.id))
                        else:
                            flash('Tests successfully run in %f' % run_time, 'ok')
                else:
                    pass
                    
        
        c.options = self.submission
        
        languages = [(None, '---'), ]
        languages.extend((l.id, l.name) for l in self.assignment.allowed_languages)
        c.child_args['language_id'] = dict(options=languages)
        
        return dict(page='submissions', assignment=self.assignment, submission=self.submission,
                    compilation=compilation, testruns=testruns)
        

class SubmissionsController(BaseController):
    
    @expose('sauce.templates.submissions')
    def index(self, page=1):
        
        submission_query = Session.query(Submission).filter(Submission.student == request.student)
        submissions = Page(submission_query, page=page, items_per_page=10)
        
        return dict(page='submissions', submissions=submissions)
    
    @expose()
    def _lookup(self, id, *args):
        
        controller = SubmissionController(submission_id=int(id))
        return controller, args