# -*- coding: utf-8 -*-
"""
Functional test suite for the root controller.

This is an example of how functional tests can be written for controllers.

As opposed to a unit-test, which test a small unit of functionality,
functional tests exercise the whole application and its WSGI stack.

Please read http://pythonpaste.org/webtest/ for more information.

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

from sauce.tests import TestController

__all__ = ['TestRootController']


class TestRootController(TestController):
    """Tests for the method in the root controller."""

    def test_index(self):
        """The front page is working properly"""
        response = self.app.get('/')
        msg = 'Learn more'
        # You can look for specific strings:
        assert_true(msg in response)

        # You can also access a BeautifulSoup'ed response in your tests
        # (First run $ easy_install BeautifulSoup
        # and then uncomment the next two lines)

        #links = response.html.findAll('a')
        #print links
        #assert_true(links, "Mummy, there are no links here!")

#    def test_environ(self):
#        """Displaying the wsgi environ works"""
#        response = self.app.get('/environ.html')
#        assert_true('The keys in the environment are: ' in response)
#
#    def test_data(self):
#        """The data display demo works with HTML"""
#        response = self.app.get('/data.html?a=1&b=2')
#        expected1 = """<td>a</td>
#                <td>1</td>"""
#        expected2 = """<td>b</td>
#                <td>2</td>"""
#
#        assert expected1 in response, response
#        assert expected2 in response, response
#
#    def test_data_json(self):
#        """The data display demo works with JSON"""
#        resp = self.app.get('/data.json?a=1&b=2')
#        assert '"a": "1", "b": "2"' in resp, resp
#
#    def test_secc_with_manager(self):
#        """The manager can access the secure controller"""
#        # Note how authentication is forged:
#        environ = {'REMOTE_USER': 'manager'}
#        resp = self.app.get('/secc', extra_environ=environ, status=200)
#        assert 'Secure Controller here' in resp.body, resp.body
#
#    def test_secc_with_editor(self):
#        """The editor cannot access the secure controller"""
#        environ = {'REMOTE_USER': 'editor'}
#        self.app.get('/secc', extra_environ=environ, status=403)
#        # It's enough to know that authorization was denied with a 403 status
#
#    def test_secc_with_anonymous(self):
#        """Anonymous users must not access the secure controller"""
#        self.app.get('/secc', status=401)
#        # It's enough to know that authorization was denied with a 401 status
