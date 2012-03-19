'''
Created on 13.03.2012

@author: moschlar
'''

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text, DateTime, Boolean, Enum, Float
from sqlalchemy.orm import relationship, backref, deferred

from sauce.model import DeclarativeBase, submission

class Test(DeclarativeBase):
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True)
    
    type = Column(Enum('stdin_stdout', 'filein_fileout'), nullable=False, default='stdin_stdout')
    
    # determine whether test run is shown to user or not
    visible = Column(Boolean, nullable=False, default=False)
    
    # deferred loading: http://docs.sqlalchemy.org/en/latest/orm/mapper_config.html#deferred-column-loading
    input = deferred(Column(Text), group='data')
    output = deferred(Column(Text), group='data')
    
    argv = deferred(Column(String), group='data')
    
    timeout = Column(Float)
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship("Assignment", backref=backref('tests'))
    
#    def __init__(self, assignment=None, type='stdin_stdout', input='', output='', argv=''):
#        self.assignment = assignment
#        self.type = type
#        self.input = input
#        self.output = output
#        self.argv = argv
    
#    def _repr_(self):
#        return 'Test(assignment=%d, type=%s, visible=%s' % (self.assignment_id, self.type, self.visible)
    
    def _str_(self):
        return 'Test %s' % (self.id or '')
    
    def _unicode_(self):
        return u'Test %s' % (self.id or '')

class TestRun(DeclarativeBase):
    __tablename__ = 'testruns'
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    result = Column(Boolean, nullable=False, default=False)
    
    succeeded = Column(Integer, nullable=False, default=0)
    failed = Column(Integer, nullable=False, default=0)
    
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    submission = relationship("Submission", backref=backref('testruns', order_by='TestRun.date'))
    
    def __init__(self, submission=None, submission_id=None, succeeded=0, failed=0, result=False, date=None):
        if submission:
            self.submission = submission
        elif submission_id:
            self.submission_id = submission_id
        self.succeeded = succeeded
        self.failed = failed
        self.result = result
        self.date = date
    
    def _before_commit(self):
        self.result = (self.total > 0) and (self.failed == 0)
    
#    def __repr__(self):
#        return 'TestRun(submission=%d, succeeded=%d, failed=%d, result=%s, date=%s)' % (self.submission_id, self.succeeded, self.failed, self.result, self.date)
    
    def __str__(self):
        return '%s - %s' % (self.date.strftime('%d.%m.%Y %H:%M:%S'), self.result)
    
    def __unicode__(self):
        return u'%s - %s' % (self.date.strftime('%d.%m.%Y %H:%M:%S'), self.result)
    
    @property
    def total(self):
        return self.succeeded + self.failed
