# -*- coding: utf-8 -*-
"""
Test event request functionality

@since: 22.10.2014
@author: moschlar
"""
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2014 Moritz Schlarb
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
import re

import transaction

from sauce.model import Event, Lesson, Team, User, DBSession

from sauce.tests import TestController
from sauce.tests.functional.test_model_urls import extra_environ

from sauce.lib import sendmail
from nose import with_setup

__all__ = ['TestEventRequest']


class TestEventRequest(TestController):
    """Tests for the event request functionality."""

    lastmail = dict(subject='', body='')

    def setUp(self):
        super(TestEventRequest, self).setUp()
        def _sendmail(subject, body, to_addrs=None, from_addr=None):
            self.lastmail['subject'] = subject
            self.lastmail['body'] = body
            return True
        sendmail.sendmail = _sendmail

    def assert_email(self, subject=None, body=None):
        if not any(self.lastmail.values()):
            raise AssertionError('No mail sent (or captured)')
        else:
            if subject:
                assert subject in self.lastmail['subject'], '%s not in %s' % (subject, self.lastmail['subject'])
            if body:
                assert body in self.lastmail['body'], '%s not in %s' % (body, self.lastmail['body'])

    def test_request_list_fail(self):
        response = self.app.get('/events/request/', extra_environ=dict(REMOTE_USER='teacher1'), status=302)

    def test_request_list(self):
        self.app.get('/events/request/', extra_environ=dict(REMOTE_USER='manager'))

    def test_request_new(self):
        #: :type response: TestResponse
        response = self.app.get('/events/request/new', extra_environ=dict(REMOTE_USER='teacher1'))
        response.form.set('_url', 'new')
        response.form.set('name', 'New')
        response = response.form.submit(extra_environ=dict(REMOTE_USER='teacher1'))
        response = response.follow()
        response.mustcontain('awaiting administrator approval')
        self.assert_email('Event requested')

        event = Event.query.filter_by(_url='new').one()
        assert event.enabled is False

        i = event.id

        response = self.app.get('/events/request/', extra_environ=dict(REMOTE_USER='manager'))
        response.mustcontain('new', 'New')
        response = response.click(href='%d/enable' % i, extra_environ=dict(REMOTE_USER='manager'))
        self.assert_email('Event request granted')

        event = Event.query.filter_by(_url='new').one()
        assert event.enabled is True
