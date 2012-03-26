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
    
    # determine whether test run is shown to user or not
    visible = Column(Boolean, nullable=False, default=False)
    
    # deferred loading: http://docs.sqlalchemy.org/en/latest/orm/mapper_config.html#deferred-column-loading
    input = deferred(Column(PickleType), group='data')
    output = deferred(Column(PickleType), group='data')
    
    argv = deferred(Column(Unicode(255)), group='data')
    
    timeout = Column(Float)
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship('Assignment', backref=backref('tests'))
    
    def __unicode__(self):
        return u'Test %s' % (self.id or '')

class Testrun(DeclarativeBase):
    __tablename__ = 'testruns'
    __mapper_args__ = {'order_by': desc('date')}
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    
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
