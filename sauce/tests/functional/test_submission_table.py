
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
''':type app: webtest.TestApp'''


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
