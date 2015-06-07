# -*- coding: utf-8 -*-
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

from sauce.tests import load_app, setup_app, teardown_db
from sauce import model


__all__ = ['TestSubmissionTable']

app = None
''':type app: webtest.TestApp'''


def setUpModule():
    global app
    app = load_app()
    setup_app()


def tearDownModule():
    model.DBSession.remove()
    teardown_db()


class TestSubmissionTable(TestCase):

    def test_event_submissions(self):
        '''Submission table for event'''
        url = '/events/demo/submissions/'
        response = app.get(url, extra_environ={'REMOTE_USER': 'teacher1'})
        ''':type response: webtest.TestResponse'''
        response.mustcontain('Student A1', 'Student C1', 'Long Term Student 1',
            no=('Student Old1', 'Student Old2'))

    def test_lesson_submissions(self):
        '''Student Listing page on lesson admin page'''
        url = '/events/demo/lessons/2/submissions/'
        response = app.get(url, extra_environ={'REMOTE_USER': 'tutor1'})
        ''':type response: webtest.TestResponse'''
        response.mustcontain('Student C1', 'Student D1', 'Long Term Student 2',
            no=('Student A1', 'Student B1', 'Student Old1', 'Student Old2'))
