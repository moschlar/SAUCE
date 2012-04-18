# -*- coding: utf-8 -*-
'''Submission model module

@author: moschlar
'''

from time import time
from datetime import datetime
import logging

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean, PickleType
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase
from sauce.model.test import Testrun

from sauce.lib.runner import Runner
from sauce.lib.helpers import link

import transaction

log = logging.getLogger(__name__)

class Submission(DeclarativeBase):
    __tablename__ = 'submissions'
    __mapper_args__ = {'order_by': desc('date')}
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    '''Date of submission'''
    
    filename = Column(Unicode(255))
    '''The submitted filename, if any'''
    source = deferred(Column(Unicode(10485760)), group='data')
    '''The submitted source code'''
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship("Assignment", backref=backref('submissions'))
    
    language_id = Column(Integer, ForeignKey('languages.id'))
    language = relationship("Language")
    
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    student = relationship("Student", backref=backref('submissions'))
    
    complete = Column(Boolean, default=False)
    '''Whether submission is finally submitted or not'''
    
    def __unicode__(self):
        return u'Submission %s' % (self.id or '')
    
    def run_tests(self, submit=False):
        submitted=False
        with Runner(self) as r:
            start = time()
            compilation = r.compile()
            end = time()
            compilation_time = end - start
            log.debug(compilation)
            
            if not compilation or compilation.result:
                start = time()
                testruns = [testrun for testrun in r.test_visible()]
                end = time()
                run_time = end - start
                log.debug(testruns)
                log.debug(run_time)
                
                
                if [testrun for testrun in testruns if not testrun.result]:
                    #flash('Test run did not run successfully, you may not submit', 'error')
                    
                    log.debug('No submission')
                    
                else:
                    
                    if submit:
                        self.complete = True
                        
                        testresults = [test for test in r.test()]
                        
                        test_time = sum(t.runtime for t in testresults)
                        
                        log.debug(testresults)
                        log.debug(test_time)
                        
                        #if False in (t.result for t in testresults):
                        #    self.submission.result = False
                        #else:
                        #    self.submission.result = True
                        
                        for t in testresults:
                            self.testruns.append(Testrun(runtime=t.runtime, test=t.test, 
                                                        result=t.result, partial=t.partial, 
                                                        submission=self,
                                                        output_data=t.output_data, error_data=t.error_data))
                        
                        #if self.result:
                        #    flash('All tests completed. Runtime: %f' % test_time, 'ok')
                        #else:
                        #    flash('Tests failed. Runtime: %f' % test_time, 'error')
                        transaction.commit()
                        log.debug(self.result)
                        submitted=True
                        #transaction.commit()
                        #self.submission = DBSession.merge(self.submission)
                        #redirect(url('/submissions/%d' % self.submission.id))
                    else:
                        #flash('Tests successfully run in %f' % run_time, 'ok')
                        log.debug('Tests sucessfully run')
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
        return self.student.team_by_event(self.assignment.event)
    
    @property
    def result(self):
        if self.testruns:
            for t in self.testruns:
                if not t.result:
                    return False
            return True
        return False
    
    @property
    def runtime(self):
        return sum(t.runtime for t in self.testruns)
    
    @classmethod
    def by_assignment_and_student(cls, assignment, student):
        return cls.query.filter_by(assignment_id=assignment.id).filter_by(student_id=student.id)
    

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
    
    grade = Column(Integer)
