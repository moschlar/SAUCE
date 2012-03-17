'''
Created on 13.03.2012

@author: moschlar
'''

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship, backref, deferred

from sauce.model import DeclarativeBase

class Test(DeclarativeBase):
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True)
    
    type = Column(Enum('stdin_stdout', 'filein_fileout'))
    
    # determine whether test run is shown to user or not
    visible = Column(Boolean)
    
    # deferred loading: http://docs.sqlalchemy.org/en/latest/orm/mapper_config.html#deferred-column-loading
    input = deferred(Column(Text), group='data')
    output = deferred(Column(Text), group='data')
    
    argv = deferred(Column(String), group='data')
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship("Assignment", backref=backref('tests'))
    
    def __init__(self, type, assignment, visible=False, argv='', input='', output=''):
        self.type = type
        self.assignment = assignment
        self.visible = visible
        if argv:
            self.argv = argv
        if input:
            self.input = input
        if output:
            self.output = output
    
    def __repr__(self):
        return '<Test>'

class TestRun(DeclarativeBase):
    __tablename__ = 'testruns'
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime)
    
    result = Column(Boolean)
    
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    submission = relationship("Submission", backref=backref('testruns'))
    
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    test = relationship("Test", backref=backref('testruns'))
    
    def __init__(self, test, submission, result=False, date=datetime.now()):
        self.test = test
        self.submission = submission
        self.result = result
        self.date = date
    
    def __repr__(self):
        return '<TestRun>'