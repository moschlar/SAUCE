'''
Created on 13.03.2012

@author: moschlar
'''

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase

class Submission(DeclarativeBase):
    __tablename__ = 'submissions'
    __mapper_args__ = {'order_by': desc('date')}
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    source = Column(Unicode)
    filename = Column(Unicode(255))
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship("Assignment", backref=backref('submissions'))
    
    language_id = Column(Integer, ForeignKey('languages.id'), nullable=False)
    language = relationship("Language")
    
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    student = relationship("Student", backref=backref('submissions'))
    
    complete = Column(Boolean, default=False)
    
    testrun_id = Column(Integer, ForeignKey('testruns.id'))
    testrun = relationship('TestRun', backref=backref('submission', uselist=False))
    
#    def __init__(self, assignment, language, student, date=None):
#        self.assignment = assignment
#        self.language = language
#        self.student = student
#        self.date = date or datetime.now()
    
#    def __repr__(self):
#        return 'Submission()'
    
    def __str__(self):
        return 'Submission %s' % (self.id or '')
    
    def __unicode__(self):
        return u'Submission %s' % (self.id or '')
