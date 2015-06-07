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

from urllib import urlencode
from urlparse import urljoin

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

    menu_items = [urljoin('/events/demo/admin/', link)
        for link in ('./events/', './tutors/', './lessons/', './teams/', './students/',
            './sheets/', './assignments/', './tests/', './newsitems/')]

    def test_toplevel(self):
        '''Toplevel menu items on event admin page'''
        url = '/events/demo/admin/'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_firstlevel(self):
        '''First level menu items on event admin page'''
        url = '/events/demo/admin/students/'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_new(self):
        '''New page menu items on event admin page'''
        url = '/events/demo/admin/students/new'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_edit(self):
        '''Edit page menu items on event admin page'''
        url = '/events/demo/admin/students/6/edit'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_edit_post(self):
        '''Edit post page menu items on event admin page'''
        url = '/events/demo/admin/students/6/'
        response = app.post(url, extra_environ=self.environ,
            params=urlencode({'sprox_id': '', 'id': 6, '_method': 'PUT', 'email_address': 'blarb', }))
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_delete(self):
        '''Delete page menu items on event admin page'''
        url = '/events/demo/admin/students/6/delete'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)


class TestLessonController(TestCase):

    environ = {'REMOTE_USER': 'teacher1'}

    menu_items = [urljoin('/events/demo/lessons/1/', link)
        for link in ('./lessons/', './tutors/', './teams/', './students/')]

    def test_toplevel(self):
        '''Toplevel menu items on lessons admin page'''
        url = '/events/demo/lessons/1/'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_firstlevel(self):
        '''First level menu items on lessons admin page'''
        url = '/events/demo/lessons/1/students/'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_new(self):
        '''New page menu items on lessons admin page'''
        url = '/events/demo/lessons/1/students/new'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_edit(self):
        '''Edit page menu items on lessons admin page'''
        url = '/events/demo/lessons/1/students/6/edit'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)

    def test_edit_post(self):
        '''Edit post page menu items on lessons admin page'''
        url = '/events/demo/lessons/1/students/6/'
        response = app.post(url, extra_environ=self.environ,
            params=urlencode({'sprox_id': '', 'id': 6, '_method': 'PUT', 'email_address': 'blarb', }))
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        self.assertEqual(self.menu_items, menu_items)
