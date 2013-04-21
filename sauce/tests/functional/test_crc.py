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

import nose.tools as nt
try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from urllib import urlencode
from urlparse import urljoin

from os import path
from tg import config
from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from webtest import TestApp

from sauce.tests import teardown_db
from sauce import model


__all__ = ['']

app = None

def setUpModule():
    # Loading the application:
    conf_dir = config.here
    wsgiapp = loadapp('config:test.ini#main_without_authn',
                      relative_to=conf_dir)
    global app
    app = TestApp(wsgiapp)
    # Setting it up:
    test_file = path.join(conf_dir, 'test.ini')
    cmd = SetupCommand('setup-app')
    cmd.run([test_file])


def tearDownModule():
    model.DBSession.remove()
    teardown_db()


class TestEventAdminController(TestCase):

    environ = {'REMOTE_USER': 'teacher1'}

    def test_assignments_table(self):
        url = '/events/demo/admin/assignments/'
        response = app.get(url, extra_environ=self.environ)
        self.assertIn('Square it', response)
        self.assertNotIn('Find the Start button', response)

    def test_assignments_new(self):
        url = '/events/demo/admin/assignments/new'
        response = app.get(url, extra_environ=self.environ)
        self.assertIn('Sheet 1', response)
        self.assertNotIn('Learning Windows(TM) 95', response)

    def test_students_table(self):
        url = '/events/demo/admin/students/'
        response = app.get(url, extra_environ=self.environ)
        self.assertIn('studente1', response)
        self.assertNotIn('studentold1', response)
        self.assertNotIn('Team Old A', response)
        self.assertNotIn('Lesson Old A', response)

    def test_students_new(self):
        url = '/events/demo/admin/students/new'
        response = app.get(url, extra_environ=self.environ)
        self.assertNotIn('Team Old A', response)
        self.assertNotIn('Lesson Old A', response)
