# -*- coding: utf-8 -*-
"""
"""

import nose.tools as nt
from unittest.case import TestCase

from urllib import urlencode
from urlparse import urljoin

from os import path
from tg import config
from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from webtest import TestApp

from sauce.tests import teardown_db
from sauce import model

__all__ = ['TestEventAdminController', 'TestLessonController']

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

    menu_items = [urljoin('/events/demo/admin/', link)
        for link in ('./events/', './tutors/', './lessons/', './teams/', './students/',
            './sheets/', './assignments/', './tests/', )]

    def test_toplevel(self):
        url = '/events/demo/admin/'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_firstlevel(self):
        url = '/events/demo/admin/students/'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_new(self):
        url = '/events/demo/admin/students/new'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_edit(self):
        url = '/events/demo/admin/students/6/edit'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_edit_post(self):
        url = '/events/demo/admin/students/6/'
        response = app.post(url, extra_environ=self.environ,
            params=urlencode({'sprox_id': '', 'id': 6, '_method': 'PUT', 'email_address': 'blarb', }))
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_delete(self):
        url = '/events/demo/admin/students/6/delete'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)


class TestLessonController(TestCase):

    environ = {'REMOTE_USER': 'teacher1'}

    menu_items = [urljoin('/events/demo/lessons/1/', link)
        for link in ('./lessons/', './tutors/', './teams/', './students/')]

    def test_toplevel(self):
        url = '/events/demo/lessons/1/'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_firstlevel(self):
        url = '/events/demo/lessons/1/students/'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_new(self):
        url = '/events/demo/lessons/1/students/new'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_edit(self):
        url = '/events/demo/lessons/1/students/6/edit'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_edit_post(self):
        url = '/events/demo/lessons/1/students/6/'
        response = app.post(url, extra_environ=self.environ,
            params=urlencode({'sprox_id': '', 'id': 6, '_method': 'PUT', 'email_address': 'blarb', }))
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)

    def test_delete(self):
        url = '/events/demo/lessons/1/students/6/delete'
        response = app.get(url, extra_environ=self.environ)
        m = response.html.find('div', {'id': 'menu_items'})
        menu_items = [urljoin(url, link['href']) for link in m.findAll('a')]
        nt.assert_equal(self.menu_items, menu_items)
