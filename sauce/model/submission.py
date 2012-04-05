# -*- coding: utf-8 -*-
'''Submission model module'''

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean, PickleType
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase

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
    
    language_id = Column(Integer, ForeignKey('languages.id'), nullable=False)
    language = relationship("Language")
    
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    student = relationship("Student", backref=backref('submissions'))
    
    complete = Column(Boolean, default=False)
    '''Whether submission is finally submitted or not'''
    
    def __unicode__(self):
        return u'Submission %s' % (self.id or '')
    
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
    