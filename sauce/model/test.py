# -*- coding: utf-8 -*-
'''Test model module'''

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean, Enum, Float, PickleType
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase

class Test(DeclarativeBase):
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True)
    
    type = Column(Enum('stdin_stdout', 'filein_fileout'), nullable=False, default='stdin_stdout')
    
    # Validator options
    
    # Output ignore options
    ignore_case = Column(Boolean, nullable=False, default=True)
    '''Call .upper() on output before comparison'''
    ignore_whitespace = Column(Boolean, nullable=False, default=True)
    '''Call .split() on every line of output before comparison'''
    ignore_lines = Column(Boolean, nullable=False, default=False)
    '''Call .split() on full output before comparison'''
    
    # Output parsing options
    parse_int = Column(Boolean, nullable=False, default=False)
    '''Parse every substring in output to int before comparison'''
    parse_float = Column(Boolean, nullable=False, default=False)
    '''Parse every substring in output to float before comparison'''
    
    # /Validator options
    
    visible = Column(Boolean, nullable=False, default=False)
    '''Whether test is shown to user or not'''
    
    input = deferred(Column(Unicode(10485760)), group='data')
    output = deferred(Column(Unicode(10485760)), group='data')
    
    argv = deferred(Column(Unicode(255)), group='data')
    '''Command line arguments'''
    
    _timeout = Column('timeout', Float)
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship('Assignment', backref=backref('tests'))
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', backref=backref('tests'))
    
    def __unicode__(self):
        return u'Test %s' % (self.id or '')
    
    @property
    def timeout(self):
        return self._timeout or self.assignment.timeout

class Testrun(DeclarativeBase):
    __tablename__ = 'testruns'
    __mapper_args__ = {'order_by': desc('date')}
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    stdout = deferred(Column(Unicode(10485760)), group='data')
    stderr = deferred(Column(Unicode(10485760)), group='data')
    
    runtime = Column(Float)
    
    result = Column(Boolean, nullable=False, default=False)
    
    succeeded = Column(Integer, nullable=False, default=0)
    failed = Column(Integer, nullable=False, default=0)
    
    def _before_commit(self):
        self.result = (self.total > 0) and (self.failed == 0)
    
    def __str__(self):
        return '%s - %s' % (self.date.strftime('%d.%m.%Y %H:%M:%S'), self.result)
    
    def __unicode__(self):
        return u'%s - %s' % (self.date.strftime('%d.%m.%Y %H:%M:%S'), self.result)
    
    @property
    def total(self):
        return self.succeeded + self.failed
