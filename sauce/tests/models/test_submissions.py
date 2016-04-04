# -*- coding: utf-8 -*-
'''
Created on Mar 12, 2014

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

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from sauce.model import Assignment, Submission

__all__ = ['TestSubmission']


class TestSubmission(TestCase):

    def test_submission_full_source(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD',
            submission_scaffold_foot=u'FOOT',
        )
        s = Submission(
            id=4711,
            assignment=a,
            source=u'BODY',
        )
        assert s.full_source == u'HEAD\nBODY\nFOOT', s.full_source
