# -*- coding: utf-8 -*-
'''Test model module

@author: moschlar
'''
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
from datetime import datetime
from warnings import warn

try:
    from nose.tools import nottest
except ImportError:
    from decorator import decorator
    nottest = decorator

from sqlalchemy import Column, ForeignKey, Index
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean, Enum, Float
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.sql import asc

from sauce.model import DeclarativeBase

log = logging.getLogger(__name__)


@nottest
class Test(DeclarativeBase):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode(255), nullable=True, default=None)

    _visible = Column('visible', Boolean, nullable=True, default=False)
    '''Whether test is shown to user or not'''

    result_public = Column(Boolean, nullable=False, default=True,
        doc='Whether test result is shown to the user')
    data_public = Column(Boolean, nullable=False, default=False,
        doc='Whether test input and output data is shown to the user')

    input_type = Column(Enum(u'stdin', u'file', name='test_input_type'), nullable=False, default=u'stdin')
    '''Input data type'''
    output_type = Column(Enum(u'stdout', u'file', name='test_output_type'), nullable=False, default=u'stdout')
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

    failsafe_parsing = Column(Boolean, nullable=False, default=False)  # default=False as long as the mode is not implemented
    '''Kind of like the builtin encode/decode errors keyword ignore/strict'''

    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False, index=True)
    assignment = relationship('Assignment',
        backref=backref('tests',
            order_by=id,
            cascade='all, delete-orphan')
        )
    '''Assignment this test belongs to'''

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User',
        #backref=backref('tests',
        #    cascade='all, delete-orphan')
    )
    '''User who created this test'''

    def __unicode__(self):
        return u'Test %s for Assignment %s' % (self.id or '', self.assignment.id or '')

    @property
    def visible(self):
        warn('The visible attribute is deprecated', DeprecationWarning)
        if self._visible is not None:
            return self._visible
        else:
            return self.result_public and self.data_public

    @visible.setter
    def visible(self, visible):
        warn('The visible attribute is deprecated', DeprecationWarning)
        self._visible = self.result_public = self.data_public = visible

    @property
    def parent(self):
        return self.assignment

    def convert(self, data):
        '''Performs all conversion options specified'''
        data = data.strip()
        # Normalize the values from database since they might be ''
        if self.separator:
            separator = self.separator
        else:
            separator = None

        if self.comment_prefix:
            data = '\n'.join(l.strip() for l in data.splitlines()
                if not l.strip().startswith(self.comment_prefix))
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

        sep = self.separator or u' '

        def fmt(obj):
            if self.parse_float and self.float_precision:
                try:
                    return (u'%%.%df' % self.float_precision) % obj
                except:
                    log.warn('Error converting float to string with precision', exc_info=True)
                    return unicode(obj)
            else:
                return unicode(obj)

        if self.splitlines and self.split:
            d = '\n'.join([sep.join(map(fmt, a)) for a in data])
        elif self.splitlines:
            d = '\n'.join(map(fmt, data))
        elif self.split:
            d = sep.join(map(fmt, data))
        else:
            d = fmt(data)

        # Convert to unicode again, just to be sure
        return unicode(d)

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
            log.warn('Error converting test data', exc_info=True)
            msg = u'''
There was an error converting the test data:
%s

This could be a fault in the test case,
please notify someone about this error.
''' % unicode(e.message, errors='ignore')
            return (False, False, output_test, output_data, msg)

        if output_test == output_data:
            result, partial = True, False
        elif self.show_partial_match and output_data and output_test.startswith(output_data):
            result, partial = False, True
        else:
            result, partial = False, False

        return (result, partial, output_test, output_data, u'')

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


@nottest
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

    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False, index=True)
    test = relationship('Test',
        backref=backref('testruns',
            order_by=id,
            cascade='all, delete-orphan')
        )
    '''Test that was run in this testrun'''

    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False, index=True)
    submission = relationship('Submission',
        backref=backref('testruns',
            order_by=id,
            cascade='all,delete-orphan')
        )
    '''Submission that was run in this testrun'''

    __mapper_args__ = {'order_by': asc(date)}
    __table_args__ = (Index('idx_test_submission', test_id, submission_id),)

    def __unicode__(self):
        return u'Testrun %s for Submission %d' % (self.id or '', self.submission.id or '')

    @property
    def parent(self):
        return self.test
