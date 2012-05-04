# -*- coding: utf-8 -*-
'''Test model module

@author: moschlar
'''

import logging
from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean, Enum, Float
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.sql import asc

from sauce.model import DeclarativeBase

log = logging.getLogger(__name__)

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
    '''Call .lower() on output before comparison'''
    ignore_returncode = Column(Boolean, nullable=False, default=True)
    '''Ignore test process returncode'''
    comment_prefix = Column(Unicode(16), nullable=True, default=u'#')
    '''Ignore all lines that start with comment_prefix'''
    
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
    float_precision = Column(Integer, nullable=True)
    '''The precision (number of decimal digits) to compare for floats'''
    
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
        
        # Normalize the values from database since they might be ''
        if self.separator:
            separator = self.separator
        else:
            separator = None
        
        if self.comment_prefix:
            data = '\n'.join(l.strip() for l in data.splitlines()
                               if not l.startswith(self.comment_prefix))
        else:
            data = '\n'.join(l.strip() for l in data.splitlines())
        
        if self.ignore_case:
            data = data.lower()
        
        if self.splitlines and self.split:
            d = [[ll for ll in l.split(separator) if ll]
                     for l in data.splitlines()]
        elif self.splitlines:
            d = [l for l in data.splitlines()]
        elif self.split:
            d = [l for l in data.split(separator) if l]
        else:
            d = data
        
        #TODO: If an element is not parsable, do not fail but leave element unparsed
        
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
        
        def fmt(obj):
            if self.parse_float and self.float_precision:
                try:
                    return ('%%.%df' % self.float_precision) % obj
                except:
                    log.warn('Error converting float to string with precision', exc_info=True)
                    return str(obj)
            else:
                return str(obj)
        
        if self.splitlines and self.split:
            d = '\n'.join([sep.join(map(fmt, a)) for a in data])
        elif self.splitlines:
            d = '\n'.join(map(fmt, data))
        elif self.split:
            d = sep.join(map(fmt, data))
        else:
            d = fmt(data)
        
        return d
    
    def validate(self, output_data):
        ''''''
        
        if self.output_data:
            test_output_data = self.test_output_data
        else:
            test_output_data = u''
        
        try:
            output_test = test_output_data
            output_data = self.unconvert(self.convert(output_data)).strip()
        except Exception as e:
            log.warn('Error validating test data', exc_info=True)
            msg = u'''
There was an error converting the test data:
%s
This might be an error in the test case.
Please notify someone about this error.
''' % (e.message)
            return(False, False, None, msg)
        
        if output_test == output_data:
            result, partial = True, False
        elif self.show_partial_match and output_test.startswith(output_data):
            result, partial = False, True
        else:
            result, partial = False, False
        
        return (result, partial, output_test, output_data)
    
    @property
    def test_output_data(self):
        '''Returns processed expected output data'''
        return self.unconvert(self.convert(self.output_data)).strip()
    
    @property
    def timeout(self):
        '''Return test timeout
        
        If not set on this test, the value from the assignment is used
        '''
        return self._timeout or self.assignment.timeout

class Testrun(DeclarativeBase):
    __tablename__ = 'testruns'
    
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
    
    __mapper_args__ = {'order_by': asc(date)}
    
    def __unicode__(self):
        return u'Testrun %s' % (self.id or '')
    
    
