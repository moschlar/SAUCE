# -*- coding: utf-8 -*-
'''Submission model module

@author: moschlar
'''

from time import time
from datetime import datetime
import logging

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean, PickleType, Float
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase, DBSession
from sauce.model.test import Testrun
from sauce.model.person import Student, Team
from sauce.model.event import Lesson

from sauce.lib.runner import Runner
from sauce.lib.helpers import link

log = logging.getLogger(__name__)

class Submission(DeclarativeBase):
    __tablename__ = 'submissions'
    
    id = Column(Integer, primary_key=True)
    
    created = Column(DateTime, nullable=False, default=datetime.now)
    '''Creation date of submission'''
    modified = Column(DateTime, nullable=False, default=datetime.now)
    '''Last modified date of submission'''
    
    filename = Column(Unicode(255))
    '''The submitted filename, if any'''
    source = deferred(Column(Unicode(10485760)), group='data')
    '''The submitted source code'''
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship("Assignment", backref=backref('submissions'))
    
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship("Language")
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref('submissions'))
    
    complete = Column(Boolean, default=False)
    '''Whether submission is finally submitted or not'''
    
    __mapper_args__ = {'order_by': [desc(created), desc(modified)]}
    
    def __unicode__(self):
        return u'Submission %s' % (self.id or '')
    
    def run_tests(self, submit=False):
        
        compilation = None
        submitted = False
        testruns = []
        
        with Runner(self) as r:
            # First compile, if needed
            start = time()
            compilation = r.compile()
            end = time()
            compilation_time = end - start
            log.debug('Compilation: %s' % compilation)
            
            if not compilation or compilation.result:
                # Then run visible tests
                start = time()
                testruns = [testrun for testrun in r.test_visible()]
                end = time()
                run_time = end - start
                log.debug('Visible test runtime: %f' % run_time)
                
                
                if [testrun for testrun in testruns if not testrun.result]:
                    # Visible tests failed
                    #flash('Test run did not run successfully, you may not submit', 'error')
                    
                    log.debug('Visible tests not successfully run')
                    
                else:
                    # Visible tests successfully run
                    if submit:
                        self.complete = True
                        
                        testresults = [test for test in r.test()]
                        
                        test_time = sum(t.runtime for t in testresults)
                        
                        log.debug('Test runtime: %f' % test_time)
                        
                        for t in testresults:
                            self.testruns.append(Testrun(runtime=t.runtime, test=t.test, 
                                                        result=t.result, partial=t.partial, 
                                                        submission=self,
                                                        output_data=t.output_data, error_data=t.error_data))
                        
                        DBSession.flush()
                        log.debug('Result: %s ' % self.result)
                        submitted = True
                    else:
                        #flash('Tests successfully run in %f' % run_time, 'ok')
                        log.debug('Tests sucessfully run in %f' % run_time)
            elif compilation and not compilation.result:
                 #flash('Compilation failed, see below', 'error')
                 log.debug('Compilation failed')
            else:
                pass
        
        return (compilation, testruns, submitted, self.result)
    
    @property
    def url(self):
        return '/submissions/%s' % self.id
    
    @property
    def link(self):
        return link('Submission %d' % self.id, self.url)
    
    @property
    def team(self):
        try:
            return self.student.team_by_event(self.assignment.event)
        except:
            return None
    
    @property
    def result(self):
        for t in self.testruns:
            if not t.result:
                return False
        return True
    
    @property
    def runtime(self):
        return sum(t.runtime for t in self.testruns)
    
    @classmethod
    def by_assignment_and_user(cls, assignment, user):
        return cls.query.filter_by(assignment_id=assignment.id).filter_by(user_id=user.id)
    
    @classmethod
    def by_teacher(cls, teacher):
        return cls.query.join(Submission.student).join(Student.teams).join(Team.lesson).filter(Lesson.teacher==teacher).order_by(desc(Submission.created)).order_by(desc(Submission.modified))
    

class Judgement(DeclarativeBase):
    __tablename__ = 'judgements'
    __mapper_args__ = {}
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    '''Date of judgement'''
    
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    submission = relationship('Submission', backref=backref('judgement', uselist=False))
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', backref=backref('judgements'))
    
    #testrun_id = Column(Integer, ForeignKey('testruns.id'))
    #testrun = relationship('Testrun', backref=backref('judgement', uselist=False))
    
    corrected_source = deferred(Column(Unicode(10485760)), group='data')
    '''Teacher-corrected source code'''
    
    comment = Column(Unicode(1048576))
    '''An additional comment to the whole submission'''
    
    annotations = Column(PickleType)
    ''''Per-line annotations should be a dict using line numbers as keys'''
    
    grade = Column(Float)

