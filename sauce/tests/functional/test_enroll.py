# -*- coding: utf-8 -*-
"""
Test enrolling functionality
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

from nose.tools import assert_true

import transaction

from sauce.model import Event, Lesson, Team, User, DBSession

from sauce.tests import TestController

__all__ = ['TestEnrolling']


class TestEnrolling(TestController):
    """Tests for the enrolling functionality."""

    def setUp(self):
        super(TestEnrolling, self).setUp()
        self.user = User(user_name='studentxxx', display_name='Student XXX', email_address='studentxxx@sauce.org')
        DBSession.add(self.user)
        transaction.commit()
        self.extra_environ = dict(REMOTE_USER=self.user.user_name)

    def tearDown(self):
        transaction.begin()
        super(TestEnrolling, self).tearDown()

    def configure_event(self, url, enroll, password):
        event = Event.query.filter_by(_url=url).one()
        event.enroll = enroll
        event.password = password
        transaction.commit()
        return DBSession.merge(event)

    def test_no_enroll(self):
        """Enrolling is not allowed"""
        demo = self.configure_event('demo', None, None)
        self.app.get('/events/demo/enroll', extra_environ=self.extra_environ, status=403)

    def test_enroll_event(self):
        """Enrolling for Event"""
        demo = self.configure_event('demo', 'event', None)

        response = self.app.get('/events/demo/enroll', extra_environ=self.extra_environ)
        response = response.follow()
        response.mustcontain('Enrolled for Event', 'Programming 101 - Demo')
        user = DBSession.merge(self.user)
        demo = DBSession.merge(demo)
        assert user in demo.members
        assert demo in user._events

    def test_enroll_password(self):
        """Enrolling for Event with password field"""
        demo = self.configure_event('demo', 'event', 'abc')

        response = self.app.get('/events/demo/enroll', extra_environ=self.extra_environ)
        response.mustcontain('Password')

    def test_enroll_password_wrong(self):
        """Enrolling for Event with wrong password"""
        demo = self.configure_event('demo', 'event', 'abc')

        response = self.app.get('/events/demo/enroll', params={'password': 'def'}, extra_environ=self.extra_environ)
        response.mustcontain('Wrong password')

    def test_enroll_password_right(self):
        """Enrolling for Event with correct password"""
        demo = self.configure_event('demo', 'event', 'abc')

        response = self.app.get('/events/demo/enroll', params={'password': 'abc'}, extra_environ=self.extra_environ)
        response = response.follow()
        response.mustcontain('Enrolled for Event', 'Programming 101 - Demo')

    def test_enroll_lesson(self):
        """Enrolling for Lesson"""
        demo = self.configure_event('demo', 'lesson', None)

        response = self.app.get('/events/demo/enroll', extra_environ=self.extra_environ)
        response.mustcontain('Lesson A/B', 'Lesson C/D', 'Lesson E')

        response.form.set('lesson', 1)
        response = response.form.submit(extra_environ=self.extra_environ)

        user = DBSession.merge(self.user)
        lesson = Lesson.query.filter_by(id=1).one()
        assert user in lesson.members
        assert lesson in user._lessons

    def test_enroll_team(self):
        """Enrolling for Team"""
        demo = self.configure_event('demo', 'team', None)

        response = self.app.get('/events/demo/enroll', extra_environ=self.extra_environ)
        response.mustcontain('Lesson A/B', 'Lesson C/D', 'Lesson E')

        response.form.set('lesson', 1)
        response = response.form.submit(extra_environ=self.extra_environ)

        response.mustcontain('Lesson A/B', 'Team A', 'Team B')

        response.form.set('team', 1)
        response = response.form.submit(extra_environ=self.extra_environ)

        user = DBSession.merge(self.user)
        team = Team.query.filter_by(id=1).one()
        assert user in team.members
        assert team in user.teams

    def test_enroll_team_new(self):
        """Enrolling for New Team"""
        demo = self.configure_event('demo', 'team_new', None)

        response = self.app.get('/events/demo/enroll', extra_environ=self.extra_environ)
        response.mustcontain('Lesson A/B', 'Lesson C/D', 'Lesson E')

        response.form.set('lesson', 1)
        response = response.form.submit(extra_environ=self.extra_environ)

        response.mustcontain('Lesson A/B', 'New Team', 'Team A', 'Team B')

        response.form.set('team', '__new__')
        response = response.form.submit(extra_environ=self.extra_environ)

        user = DBSession.merge(self.user)
        team = Team.query.filter_by(name='New Team').one()
        assert user in team.members
        assert team in user.teams
