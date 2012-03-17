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
    
    succeeded = Column(Integer)
    failed = Column(Integer)
    
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    submission = relationship("Submission", backref=backref('testruns', order_by='TestRun.date'))
    
    test_id = Column(Integer, ForeignKey('tests.id'))
    test = relationship("Test", backref=backref('testruns'))
    
    def __init__(self,  submission, succeeded, failed, result=None, date=None):
        self.submission = submission
        self.succeeded = succeeded
        self.failed = failed
        
        self.result = result or (self.failed == 0)
        
        self.date = date or datetime.now()
    
    def __repr__(self):
        return 'TestRun(submission=%d, succeeded=%d, failed=%d, result=%s, date=%s)' % (self.submission_id, self.succeeded, self.failed, self.result, self.date)
    
    def __str__(self):
        return '%s - %s' % (self.date.strftime('%d.%m.%Y %H:%M:%S'), self.result)
    
    def __unicode__(self):
        return u'%s - %s' % (self.date.strftime('%d.%m.%Y %H:%M:%S'), self.result)