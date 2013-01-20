'''
Created on 14.06.2012

@author: moschlar
'''

from os import path
import sys

from tg import config
from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from webtest import TestApp

from sauce.tests import teardown_db
from sauce import model

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


# The USERS and PATHS variables are interpreted in a matrix-like style
# USERS contain valid usernames for the REMOTE_USER variable.
# The usernames should be sorted hierarchically to make configuration
# simpler
# PATHS contains a path and expected statuses for the above usernames.
# (statuses that are not specified aren't tested, of course)
# If path[0] is a tuple or list, it will be used for recursive url generation

#   PATH                    ANONYMOUS   STUDENT     TUTOR       TEACHER     MANAGER
USERS = (                   None,       'studenta1','tutor',    'teacher',  'manager')
PATHS = (
    # All the static pages
    (('', ['/', '/index', '/about', '/contact', '/login',
        ('/docs', ['', '/', '/tests', '/deutsch', '/tips', '/Changelog', '/Roadmap'])
    ]),
                            None),
    # The language information pages
    (('/languages', ['', '/', '/1', '/2', '/3']), None),
    # The basic event-sheet-assignment pages
    (('/events', ['', '/',
        ('/demo', ['/',
            ('/sheets', ['', '/',
                ('/1', ['', '/',
                    ('/assignments', ['', '/', '/1'])
                ])
            ])
        ])
    ]),
                            None),
    (('/events/demo/sheets/1/assignments/1/similarity',
        ['', '/', '/table', '/list', '/dendrogram', '/dendrogram.png']),
                            401,        403,        None),
    ('/user',               401,        None),
    ('/admin',              401,        403,        403,        403,        None),
    (('/events/demo/admin', ['', '/', '/sheets', '/assignments', '/tests',
        '/newsitems', '/lessons', '/tutors', '/teams', '/students']),
                            401,        403,        403,        None),
    (('/events/demo/lessons/1', ['', '/', '/tutor', '/teams', '/students']),
                            401,        403,        None),
    (('/events/demo/lessons/1', ['', '/',
        ('/submissions', ['', '/',
            ('/sheet/1', ['', '/assignment/1'])
        ])
    ]),
                            401,        403,        None),
    (('/events/demo/lessons/2', ['', '/',
        ('/submissions', ['', '/',
            ('/sheet/1', ['', '/assignment/1'])
        ])
    ]),
                            401,        403,        403,        None),
    # WARNING: Submission ids come from websetup/data/course.py
    # A submission of studenta1, belonging to the lesson of tutor
    (('/submissions/25', ['', '/', '/show', '/edit', '/result']),
                            401,        None,       None,       None,       None),
    ('/submissions/25/judge',
                            401,        403,        None),
    # Team member of studenta1 submission
    (('/submissions/26', ['', '/', '/show', '/result']),
                            401,        None),
    ('/submissions/26/edit',
                            401,        403,        None),
    # A submission of studentc1, NOT belonging to the lesson of tutor
    (('/submissions/27', ['', '/', '/show', '/edit', '/result', '/judge']),
                            401,        403,        403,        None,       None),
    )


def _generate_paths(base):
    a, b = base
    for c in b:
        if isinstance(c, tuple):
            for d in _generate_paths(c):
                yield a + d
        else:
            yield a + c


def _test_path(path, user=None, status=None):
    if user:
        env = dict(REMOTE_USER=user)
    else:
        env = None
    app.get(path, extra_environ=env, status=status)


def test_paths():
    for path in PATHS:
        p, stati = path[0], path[1:]

        if isinstance(p, tuple):
            pp = _generate_paths(p)
        else:
            pp = (p, )

        for p in pp:
            for i, status in enumerate(stati):
                if status is not False:
                    user = USERS[i]
                    yield _test_path, p, user, status

