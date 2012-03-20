# -*- coding: utf-8 -*-
"""Submissionn controller module"""

import logging
from time import time

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

class SubmissionnController(BaseController):
    
    allow_only = authorize.not_anonymous()
    
    def __init__(self, assignment_id=None, submission_id=None):
        
        if bool(assignment_id) == (submission_id):
            raise Exception('Both constructor values set, that should never happen')
        
        self.submission_id = None
        
        if assignment_id:
            self.assignment_id = assignment_id
            if session.get(self.session_key):
                self.submission = session.get(self.session_key)
            else:
                self.submission = Submission()
                session[self.session_key] = self.submission
        
        if submission_id:
            self.submission_id = submission_id
            self.submission = Session.query(Submission).filter_by(id=self.submission_id).one()
            #Session.expunge(self.submission)
            #session[self.session_key] = self.submission
        
        # Now we got a self.submission in all cases
        
        if self.submission.assignment:
            self.assignment = self.submission.assignment
            self.assignment_id = self.assignment.id
        else:
            # Try to preload all needed attributes of assignment
            self.assignment = Session.query(Assignment).\
                                join(language_to_assignment).join(Test). \
                                options(joinedload(Assignment.allowed_languages), 
                                joinedload(Assignment.tests)).\
                                filter_by(id=self.assignment_id).one()
            Session.expunge(self.assignment)
        
        log.debug(self.assignment in Session)
        log.debug(self.submission in Session)
        
        #self.submission = Session.merge(self.submission)
        #self.assignment = Session.merge(self.assignment)
        
        log.debug(self.assignment in Session)
        log.debug(self.submission in Session)
        #Session.add_all((self.submission, self.assignment))
    
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
        
        log.debug('%s %s' % (self.assignment in Session, language in Session))
        log.debug('language: %s, allowed_languages: %s' % (repr(language), self.assignment.allowed_languages))    
        
        if language_id not in (l.id for l in self.assignment.allowed_languages):
            raise Exception('The Language %s is not allowed for this assignment' % (language))
            #redirect(url(request.environ['PATH_INFO']))
        
        source = ''
        try:
            source = kwargs['source']
            filename = kwargs['filename']
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
    
    
    @expose('sauce.templates.submissionn')
    def index(self, **kwargs):
        
        c.form = submission_form
        c.options = dict()
        compilation = None
        testruns = []
        
        log.debug(kwargs)
        log.debug(session)
        
        if request.environ['REQUEST_METHOD'] == 'POST':
            
            test = kwargs.get('buttons.test')
            submit = kwargs.get('buttons.submit')
            reset = kwargs.get('buttons.reset')
            
            if reset:
                del session[self.session_key]
                session.save()
                self.submission = Submission()
                flash('Resetted', 'ok')
            else:
                try:
                    (language, source, filename) = self.parse_kwargs(kwargs)
                except Exception as e:
                    flash(str(e), 'error')
                else:
                    #self.submission = Session.merge(self.submission)
                    #self.submission.assignment = self.assignment
                    # since student is not expunged from the session, we just set the id for this time
                    self.submission.student_id = request.student.id
                    self.submission.language = language
                    self.submission.source = source
                    self.submission.filename = filename
                    session[self.session_key] = self.submission
                    session.save()
                    #Session.add(self.submission)
                    #transaction.commit()
                    
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
                            
                            
#                            results = evaluateTestruns(testruns)
#                            testrun = TestRun(submission=self.submission, succeeded=results.succeeded, 
#                                              failed=results.failed, result=results.result, runtime=end - start)
#                            DBSession.add(testrun)
#                            transaction.commit()
#                        else:
#                            testruns = []
#                            results = ()
#                    submission = DBSession.query(Submission).filter(Submission.id == self.submission_id).one()
#                    return dict(page='submissions', submission=submission, compilation=compilation, 
#                                testruns=testruns, results=results)
#                
#                try:
#                        
#                        if submit:
#                            Session.add(self.submission)
#                            transaction.commit()
#                except Exception as e:
#                    raise e
#                else:
#                    flash('Saved', 'ok')
        
        c.options = self.submission
        
        languages = [(None, '---'), ]
        languages.extend((l.id, l.name) for l in self.assignment.allowed_languages)
        c.child_args = dict(language_id=dict(options=languages))
        
        return dict(page='submission', assignment_id=self.assignment_id, submission_id=self.submission_id,
                    compilation=compilation, testruns=testruns)
        raise
        #if request.environ['REQUEST_METHOD'] == 'POST':
        #    try:
        #        (language, source, filename) = self.parse_kwargs(kwargs)
        #    except Exception as e:
        #        flash(str(e), 'error')
        #        redirect(url(request.environ['PATH_INFO']))
        if not self.submission_id:
            # first call on /assigment/{id}/submission
            submission = Submission(assignment=self.assignment)
        else:
            # third call with kwargs on /submissionn/{id}
            submission = Session.query(Submission).filter_by(id=self.submission_id).one()
        
        try:
            (language, source, filename) = self.parse_kwargs(kwargs)
        except Exception as e:
            flash(str(e), 'error')
            redirect(url(request.environ['PATH_INFO']))
        
        try:
            #student = DBSession.query(Student).first()
            student = request.student
            
            #submission = Submission(assignment=self.assignment, 
            #                        language=language, 
            #                        student=student,
            #                        source=source,
            #                        filename=filename)
            
            submission.language = language
            submission.source = source
            submission.filename = filename
            submission.student = student
            
            Session.add(submission)
            transaction.commit()
        except Exception as e:
            flash(str(e), 'error')
            redirect(url(request.environ['PATH_INFO']))
        else:
            if submission not in Session:
                submission = Session.merge(submission)
            self.submission_id = submission.id
            flash('Submitted', 'ok')
            #redirect()
            c.options = dict(filename=submission.filename, source=submission.source, language=submission.language.id,
                             assignment_id=self.assignment_id, submission_id=self.submission_id)
        #else:
            # first call on /assigment/{id}/submission
            #assignment = Session.query(Assignment).filter(Assignment.id == self.assignment_id).one()
        #    c.options = dict()
        
        languages = [(None, '---'), ]
        languages.extend((l.id, l.name) for l in self.assignment.allowed_languages)
        c.child_args = dict(language=dict(options=languages))
        
        return dict(page='submission', assignment_id=self.assignment_id, 
                    submission_id=self.submission_id, compilation=compilation, testruns=testruns)

class SubmissionnsController(BaseController):
    
    @expose()
    def index(self):
        return
    
    @expose()
    def _lookup(self, id, *args):
        return SubmissionnController(submission_id=int(id)), args