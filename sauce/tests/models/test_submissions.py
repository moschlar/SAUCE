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

__all__ = ['TestAssignment', 'TestSubmission']


class TestAssignment(TestCase):

    def test_assignment_strip_scaffold(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD',
            submission_scaffold_foot=u'FOOT',
        )
        stripped = a.strip_scaffold(full_source=u'HEAD\nBODY\nFOOT')
        assert stripped == u'BODY', stripped

    def test_assignment_strip_scaffold_no(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
        )
        stripped = a.strip_scaffold(full_source=u'HEAD\nBODY\nFOOT')
        assert stripped == u'HEAD\nBODY\nFOOT', stripped

    def test_assignment_strip_scaffold_head(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD',
            # submission_scaffold_foot=u'FOOT',
        )
        stripped = a.strip_scaffold(full_source=u'HEAD\nBODY\nFOOT')
        assert stripped == u'BODY\nFOOT', stripped

    def test_assignment_strip_scaffold_foot(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            # submission_scaffold_head=u'HEAD',
            submission_scaffold_foot=u'FOOT',
        )
        stripped = a.strip_scaffold(full_source=u'HEAD\nBODY\nFOOT')
        assert stripped == u'HEAD\nBODY', stripped

    def test_assignment_strip_scaffold_head_tampered(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD',
            # submission_scaffold_foot=u'FOOT',
        )
        with self.assertRaises(Exception):
            a.strip_scaffold(full_source=u'HAED\nBODY\nFOOT')

    def test_assignment_strip_scaffold_foot_tampered(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            # submission_scaffold_head=u'HEAD',
            submission_scaffold_foot=u'FOOT',
        )
        with self.assertRaises(Exception):
            a.strip_scaffold(full_source=u'HEAD\nBODY\nFÖÖT')


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

    def test_submission_full_source_whitespace_scaffold_trailing_newline(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD\n',
            submission_scaffold_foot=u'\nFOOT',
        )
        s = Submission(
            id=4711,
            assignment=a,
            source=u'BODY',
        )
        assert s.full_source == u'HEAD\n\nBODY\n\nFOOT', s.full_source

    def test_submission_full_source_whitespace_body_trailing_newline(self):
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
            source=u'\nBODY\n',
        )
        assert s.full_source == u'HEAD\n\nBODY\n\nFOOT', s.full_source

    def test_submission_full_source_whitespace_both_trailing_newline(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD\n',
            submission_scaffold_foot=u'\nFOOT',
        )
        s = Submission(
            id=4711,
            assignment=a,
            source=u'\nBODY\n',
        )
        assert s.full_source == u'HEAD\n\n\nBODY\n\n\nFOOT', s.full_source

    def test_submission_scaffold_lines(self):
        scaffold_head = u'HEAD1\nHEAD2\nHEAD3'
        scaffold_foot = u'FOOT1\nFOOT2\nFOOT3'
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=scaffold_head,
            submission_scaffold_foot=scaffold_foot,
        )
        s = Submission(
            id=4711,
            assignment=a,
            source=u'BODY1\nBODY2\n',
        )
        assert s.scaffold_head_lines == scaffold_head.splitlines(),\
            (s.scaffold_head_lines, scaffold_head.splitlines())
        assert s.scaffold_foot_lines == scaffold_foot.splitlines(), \
            (s.scaffold_foot_lines, scaffold_foot.splitlines())

    def test_submission_scaffold_len(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD1\nHEAD2\nHEAD3',
            submission_scaffold_foot=u'FOOT1\nFOOT2\nFOOT3',
        )
        s = Submission(
            id=4711,
            assignment=a,
            source=u'BODY1\nBODY2\n',
        )
        assert s.scaffold_head_lines_len == 3, s.scaffold_head_lines_len
        assert s.scaffold_foot_lines_len == 3, s.scaffold_foot_lines_len

    def test_submission_scaffold_len_trailing_newline(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD1\nHEAD2\nHEAD3\n',
            submission_scaffold_foot=u'FOOT1\nFOOT2\nFOOT3\n',
        )
        s = Submission(
            id=4711,
            assignment=a,
            source=u'BODY1\nBODY2\n',
        )
        assert s.scaffold_head_lines_len == 3, s.scaffold_head_lines_len
        assert s.scaffold_foot_lines_len == 3, s.scaffold_foot_lines_len

    def test_submission_scaffold_line_numbers(self):
        a = Assignment(
            id=13,
            sheet_id=42,
            assignment_id=1337,
            submission_scaffold_head=u'HEAD1\nHEAD2\nHEAD3\n',
            submission_scaffold_foot=u'FOOT1\nFOOT2\nFOOT3\n',
        )
        s = Submission(
            id=4711,
            assignment=a,
            source=u'BODY1\nBODY2\n',
        )
        start_head, end_head, start_foot, end_foot = s.scaffold_line_numbers
        assert start_head == 0, start_head
        assert end_head == 3, end_head
        assert start_foot == 5, start_foot
        assert end_foot == 8, end_foot
