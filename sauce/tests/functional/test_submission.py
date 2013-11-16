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


class TestSubmissionController(TestCase):

    environ = {'REMOTE_USER': 'tutor1'}

    def test_submission_lifecycle(self):
        kw = dict(extra_environ=self.environ)
        url = '/events/demo/sheets/1/assignments/1/submit'

        response = app.get(url, **kw)
        url = response.location[len('http://localhost'):-len('/edit')]
        print url
        response = response.follow(**kw)

        response.form.set('filename', 'subm.txt')
        response.form.set('source', 'code')
        response = response.form.submit(**kw)
        response = response.follow(**kw)

        response = app.get(url + '/show', **kw)

        response = app.get(url + '/public', **kw)

        response = app.get(url + '/show', extra_environ={'REMOTE_USER': 'studenta1'})

        response = app.get(url + '/public', **kw)

        response = app.get(url + '/judge', **kw)
        response.form.set('comment', 'nope')
        response.form.set('corrected_source', 'Code')
        response.form.set('grade', '0.42')
        response = response.form.submit(**kw)
        response = response.follow(**kw)

        response = app.get(url + '/delete', **kw)
