# -*- coding: utf-8 -*-
"""
"""
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


__all__ = ['TestEventAdminController', 'TestLessonController']

app = None
''':type app: webtest.TestApp'''


def setUpModule():
    global app
    app = load_app()
    setup_app()


def tearDownModule():
    model.DBSession.remove()
    teardown_db()


class TestEventAdminController(TestCase):

    environ = {'REMOTE_USER': 'teacher1'}

    def test_assignments_table(self):
        '''Assignment Listing page on event admin page'''
        url = '/events/demo/admin/assignments/'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('Square it',
            no=('Find the Start button', ))

    def test_assignments_new(self):
        '''New Assignment page on event admin page'''
        url = '/events/demo/admin/assignments/new'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('Sheet 1',
            no=('Learning Windows(TM) 95', ))

    def test_students_table(self):
        '''Student Listing page on event admin page'''
        url = '/events/demo/admin/students/'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('studente1',
            no=('studentold1', 'Team Old A', 'Lesson Old A'))

    def test_students_new(self):
        '''New Student page on event admin page'''
        url = '/events/demo/admin/students/new'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain(no=('Team Old A', 'Lesson Old A', ))

    def test_teams_table(self):
        '''Team Listing page on event admin page'''
        url = '/events/demo/admin/teams/'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('Team A', 'Team B', 'Lesson C/D', 'Student D3',
            no=('Student Old 1', 'Team Old A', 'Lesson Old A'))

    def test_tutor_table(self):
        '''Tutors Listing page on event admin page'''
        url = '/events/demo/admin/tutors/'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('tutor1', 'Dr. Tutor',
            'tutor2', 'M. Sc. Tutor', 'teacher1', 'Prof. Dr. Teacher',
            'Lesson A/B', 'Lesson C/D', 'Lesson E',
            no=('Lesson Old A'))


class TestLessonController(TestCase):

    environ = {'REMOTE_USER': 'tutor1'}

    def test_students_table(self):
        '''Student Listing page on lesson admin page'''
        url = '/events/demo/lessons/2/students/'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('studentc1', 'studentd3', 'Team C', 'Team D',
            no=('studenta1', 'Team A'))

    def test_teams_table(self):
        '''Team Listing page on lesson admin page'''
        url = '/events/demo/lessons/2/teams/'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('Team C', 'Student C1', 'Lesson C/D',
            no=('Team A', 'Team B', 'Student A1', 'Student B1', 'Lesson A/B'))

    def test_tutor_table(self):
        '''Tutors Listing page on lesson admin page'''
        url = '/events/demo/lessons/2/tutors/'
        response = app.get(url, extra_environ=self.environ)
        ''':type response: webtest.TestResponse'''
        response.mustcontain('tutor1', 'Dr. Tutor', 'Lesson C/D',
            no=('tutor2', 'M. Sc. Tutor', 'teacher1', 'Prof. Dr. Teacher', 'Lesson A/B', 'Lesson E'))

