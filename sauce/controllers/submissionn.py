# -*- coding: utf-8 -*-
"""Submissionn controller module"""

import logging
from time import time

from collections import namedtuple

# turbogears imports
from tg import expose, request, redirect, url, flash, session, tmpl_context as c
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
from repoze.what import predicates, authorize

from sqlalchemy.orm import joinedload #, joinedload_all, subqueryload, immediateload
from sqlalchemy.orm.exc import NoResultFound
import transaction

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession as Session, Assignment, Submission, Language
from sauce.model.assignment import language_to_assignment
from sauce.model.test import Test

from sauce.lib.runner import Runner

from sauce.widgets.submission import submission_form

log = logging.getLogger(__name__)
results = namedtuple('results', ('result', 'ok', 'fail', 'total'))

class SubmissionnController(BaseController):
    
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
    
    @property
    def session_key(self):
        return 'ass%dsub' % self.assignment_id
    
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
    
    @expose('sauce.templates.submissionn')
    def index(self, **kwargs):
        
        # Some initialization
        c.form = submission_form
        c.options = dict()
        compilation = None
        testruns = []
        submit = None
        
        log.debug(kwargs)
        log.debug(session)
        
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
                    
        if self.submission:
            with Runner(self.submission) as r:
                start = time()
                compilation = r.compile()
                end = time()
                compilation_time = end-start
                log.debug(compilation)
                
                if not compilation or compilation.returncode == 0:
                    start = time()
                    testruns = [testrun for testrun in r.test_visible()]
                    end = time()
                    run_time = end-start
                    log.debug(testruns)
                    
                    if submit:
                        #log.debug('submit')
                        if [testrun for testrun in testruns if not testrun.result]:
                            flash('Test run did not run successfully, you may not submit', 'error')
                        else:
                            self.submission.complete = True
                            
                            start = time()
                            tests = [test for test in r.test()]
                            end = time()
                            test_time = end-start
                            
                            testresults = self.evalTests(tests)
                            log.debug('%f %s %s %s %s' % (test_time, testresults.result, testresults.ok, 
                                                       testresults.fail, testresults.total))
                            
                            self.submission.result = testresults.result
                            flash('Test result: %s' % testresults.result, 'info')
                            
                            transaction.commit()
                            self.submission = Session.merge(self.submission)
                            
        
        c.options = self.submission
        
        languages = [(None, '---'), ]
        languages.extend((l.id, l.name) for l in self.assignment.allowed_languages)
        c.child_args = dict(language_id=dict(options=languages))
        
        return dict(page='submission', assignment=self.assignment, submission=self.submission,
                    compilation=compilation, testruns=testruns)
        

class SubmissionnsController(BaseController):
    
    @expose()
    def index(self):
        return
    
    @expose()
    def _lookup(self, id, *args):
        return SubmissionnController(submission_id=int(id)), args