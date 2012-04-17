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
    
    input_type = Column(Enum(u'stdin', u'file'), nullable=False, default=u'stdin')
    '''Input data type'''
    output_type = Column(Enum(u'stdout', u'file'), nullable=False, default=u'stdout')
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
    ignore_returncode = Column(Boolean, nullable=False, default=False)
    '''Ignore test process returncode'''
    
    show_partial_match = Column(Boolean, nullable=False, default=True)
    '''Recognize partial match'''
    
    # Output splitting options
    separator = Column(Unicode(16), default=None)
    '''The separator string to use for .split()
    Defaults to None (whitespace)'''
    splitlines = Column(Boolean, nullable=False, default=False)
    '''Call .splitlines() on full output before comparison'''
    split = Column(Boolean, nullable=False, default=True)
    '''Call .split() on full output of output before comparison
    or on each line from .splitlines() if splitlines is set'''
    sort = Column(Boolean, nullable=False, default=False)
    '''Sort output and test data before comparison
    Parsing is performed first, if enabled
    Results depends on whether splitlines and/or split are set:
    if split and splitlines:
        2-dimensional array in which only the second dimension 
        is sorted (e.g. [[3, 4], [1, 2]])
    if only split or only splitlines:
        1-dimensional list is sorted by the types default comparator
    '''
    
    # Output parsing options
    parse_int = Column(Boolean, nullable=False, default=False)
    '''Parse every substring in output to int before comparison'''
    parse_float = Column(Boolean, nullable=False, default=False)
    '''Parse every substring in output to float before comparison'''
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship('Assignment', backref=backref('tests'))
    '''Assignment this test belongs to'''
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher', backref=backref('tests'))
    '''Teacher who created this test'''
    
    def __unicode__(self):
        return u'Test %s' % (self.id or '')
    
    def convert(self, data):
        '''Performs all conversion options specified'''
        
        if self.splitlines and self.split:
            d = [l.split(self.separator) for l in data.splitlines()]
        elif self.splitlines:
            d = data.splitlines()
        elif self.split:
            d = data.split(self.separator)
        else:
            d = data
        
        if self.parse_float:
            if self.splitlines and self.split:
                d = [[float(b) for b in a] for a in d]
            elif self.splitlines or self.split:
                d = [float(a) for a in d]
            else:
                d = float(d)
        if self.parse_int:
            if self.splitlines and self.split:
                d = [[int(b) for b in a] for a in d]
            elif self.splitlines or self.split:
                d = [int(a) for a in d]
            else:
                d = int(d)
        
        if self.sort:
            if self.splitlines and self.split:
                d = [sorted(a) for a in d]
            elif self.splitlines or self.split:
                d = sorted(d)
        
        return d
    
    def unconvert(self, data):
        '''Reverts the conversions from convert'''
        
        sep = self.separator or ' '
        
        if self.splitlines and self.split:
            d = '\n'.join([sep.join(map(str, a)) for a in data])
        elif self.splitlines:
            d = '\n'.join(map(str, data))
        elif self.split:
            d = sep.join(map(str, data))
        else:
            d = str(data)
        
        return d
    
    def validate(self, output):
        ''''''
        
        test_output = self.unconvert(self.convert(self.output_data))
        run_output = self.unconvert(self.convert(output))
        
        if test_output == run_output:
            result, partial = True, False
        elif self.show_partial_match and test_output.startswith(run_output):
            result, partial = False, True
        else:
            result, partial = False, False
        
        return (result, partial, test_output, run_output)
    
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
    partial = Column(Boolean, nullable=False, default=False)
    
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    test = relationship('Test', backref=backref('testruns'))
    '''Test that was run in this testrun'''
    
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    submission = relationship('Submission', backref=backref('testruns'))
    '''Submission that was run in this testrun'''
    
    def __unicode__(self):
        return u'Testrun %s' % (self.id or '')
    
    
