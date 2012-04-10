# -*- coding: utf-8 -*-
'''Test model module

@author: moschlar
'''

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean, Enum, Float, PickleType
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase

class Test(DeclarativeBase):
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True)
    
    visible = Column(Boolean, nullable=False, default=False)
    '''Whether test is shown to user or not'''
    
    input_type = Column(Enum('stdin', 'file'), nullable=False, default='stdin')
    '''Input data type'''
    output_type = Column(Enum('stdout', 'file'), nullable=False, default='stdout')
    '''Output data type'''
    
    input_filename = Column(Unicode(255))
    '''Input data filename'''
    output_filename = Column(Unicode(255))
    '''Output data filename'''
    
    argv = deferred(Column(Unicode(255)), group='data')
    '''Command line arguments
    
    Possible variables are:
        {path}: Absolute path to temporary working directory
        {infile}: Full path to test input file
        {outfile}: Full path to test output file
    '''
    
    input_data = deferred(Column(Unicode(10485760)), group='data')
    output_data = deferred(Column(Unicode(10485760)), group='data')
    
    _timeout = Column('timeout', Float)
    
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
    sort = Column(Boolean, nullable=False, default=False)
    '''Sort output and test data before comparison'''
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship('Assignment', backref=backref('tests'))
    '''Assignment this test belongs to'''
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher', backref=backref('tests'))
    '''Teacher who created this test'''
    
    def __unicode__(self):
        return u'Test %s' % (self.id or '')
    
    @property
    def timeout(self):
        '''Return test timeout
        
        If not set on this test, the value from the assignment is used
        '''
        return self._timeout or self.assignment.timeout

class Testrun(DeclarativeBase):
    __tablename__ = 'testruns'
    __mapper_args__ = {'order_by': desc('date')}
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    output_data = deferred(Column(Unicode(10485760)), group='data')
    '''Output data from testrun
    
    Captured from stdout or content of test output file, depending
    on the test specification
    '''
    error_data = deferred(Column(Unicode(10485760)), group='data')
    '''Error data from testrun (stderr)'''
    
    runtime = Column(Float)
    
    result = Column(Boolean, nullable=False, default=False)
    
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    test = relationship('Test', backref=backref('testruns'))
    '''Test that was run in this testrun'''
    
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    submission = relationship('Submission', backref=backref('testruns'))
    '''Submission that was run in this testrun'''
    
    def __unicode__(self):
        return u'Testrun %s' % (self.id or '')
    
    
