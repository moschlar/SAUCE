# -*- coding: utf-8 -*-
"""Submissionn controller module"""

import logging
from time import time

from collections import namedtuple

# turbogears imports
from tg import expose, request, redirect, url, flash, session, abort, tmpl_context as c
#from tg import redirect, validate, flash
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
from repoze.what import predicates, authorize

from sqlalchemy.orm import joinedload #, joinedload_all, subqueryload, immediateload
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import transaction

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, Assignment, Submission, Language, Testrun, Event

from sauce.lib.runner import Runner

from sauce.widgets.submission import submission_form
from sauce.lib.auth import has_student
from repoze.what.predicates import not_anonymous

log = logging.getLogger(__name__)
results = namedtuple('results', ('result', 'ok', 'fail', 'total'))

class SubmissionController(BaseController):
    
    allow_only = authorize.not_anonymous()
    
    def __init__(self, assignment=None, submission=None):
        
        if bool(assignment) == bool(submission):
            raise Exception('Both constructor values set, that should never happen')
        
        self.submission_id = None
        
        if assignment:
            self.assignment = assignment
            self.submission = Submission()
        
        if submission:
            self.submission = submission
            self.assignment = self.submission.assignment
            
            self.allow_only = has_student(type=Submission, id=submission.id, 
                                      msg='You may only view your own submissions')
        
        self.event = self.assignment.event
    
    def parse_kwargs(self, kwargs):
        
        # Get language from kwargs
        try:
            language_id = int(kwargs['language_id'])
        except KeyError:
            raise Exception('No language selected')
            #redirect(url(request.environ['PATH_INFO']))
        except ValueError:
            raise Exception('No language selected')
            #redirect(url(request.environ['PATH_INFO']))
        else:
            language = DBSession.query(Language).filter_by(id=language_id).one()
        
        #log.debug('%s %s' % (self.assignment in Session, language in Session))
        #log.debug('language: %s, allowed_languages: %s' % (repr(language), self.assignment.allowed_languages))    
        
        if language not in self.assignment.allowed_languages:
            raise Exception('The language %s is not allowed for this assignment' % (language))
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
                try:
                    DBSession.delete(self.submission)
                except Exception as e:
                    log.debug(e)
                else:
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
                    
                    DBSession.add(self.submission)
                    transaction.commit()
                    self.submission = DBSession.merge(self.submission)
                    
        if self.submission.source and not self.submission.complete:
            with Runner(self.submission) as r:
                start = time()
                compilation = r.compile()
                end = time()
                compilation_time = end - start
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
                            
                            testresults = [test for test in r.test()]
                            
                            test_time = sum(t.runtime for t in testresults)
                            
                            if False in (t.result for t in testresults):
                                self.submission.result = False
                            else:
                                self.submission.result = True
                            
                            if self.submission.result:
                                flash('All tests completed. Runtime: %f' % test_time, 'ok')
                            else:
                                flash('Tests failed. Runtime: %f' % test_time, 'error')
                            
                            for t in testresults:
                                self.submission.testruns.append(Testrun(runtime=t.runtime,
                                                test=t.test, result=t.result, submission=self.submission,
                                                output_data=t.output_data, error_data=t.error_data))
                            
                            transaction.commit()
                            self.submission = DBSession.merge(self.submission)
                            redirect(url('/submissions/%d' % self.submission.id))
                        else:
                            flash('Tests successfully run in %f' % run_time, 'ok')
                elif compilation and compilation.returncode != 0:
                     flash('Compilation failed, see below', 'error')
                else:
                    pass
                    
        
        c.options = self.submission
        
        languages = [(None, '---'), ]
        languages.extend((l.id, l.name) for l in self.assignment.allowed_languages)
        c.child_args['language_id'] = dict(options=languages)
        
        return dict(page='submissions', event=self.event, assignment=self.assignment, submission=self.submission,
                    compilation=compilation, testruns=testruns)
        

class SubmissionsController(BaseController):
    
    allow_only = not_anonymous(msg=u'Only logged in users may see submissions')
    
    def __init__(self, assignment=None):
        
        self.assignment = assignment
        
        if self.assignment:
            self.sheet = self.assignment.sheet
            self.event = self.sheet.event
        
    @expose('sauce.templates.submissions')
    def index(self, page=1):
        
        if self.assignment:
            submission_query = Submission.by_assignment_and_student(self.assignment, request.student)
        else:
            submission_query = Submission.query.filter_by(student_id=request.student.id)
        
        submissions = Page(submission_query, page=page, items_per_page=10)
        
        return dict(page='submissions', submissions=submissions)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return SubmissionController for specified submission_id'''
        
        # Redirect to /submissions/{id}
        if len(request.environ['PATH_INFO'].split('/')) > 3:
            redirect(url('/submissions/%s' % id))
        
        try:
            id = int(id)
            submission = Submission.query.filter_by(id=id).one()
        except ValueError:
            abort(400)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        controller = SubmissionController(submission=submission)
        return controller, args
    
