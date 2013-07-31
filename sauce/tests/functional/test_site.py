'''
Created on 14.06.2012

@author: moschlar
'''
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

from os import path
import sys

from tg import config
from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from webtest import TestApp

from sauce.tests import teardown_db
from sauce import model
import transaction

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

    # Prepare authz test data
    subm_100 = model.Submission(id=100, filename=u'subm_100', source=u'subm_100',
        assignment=model.Assignment.query.filter_by(id=2).one(),
        user=model.User.query.filter_by(user_name='studentc1').one(),
        language=model.Language.query.first())
    subm_101 = model.Submission(id=101, filename=u'subm_101', source=u'subm_101',
        assignment=model.Assignment.query.filter_by(id=2).one(),
        user=model.User.query.filter_by(user_name='studentc2').one(),
        language=model.Language.query.first())
    subm_102 = model.Submission(id=102, filename=u'subm_102', source=u'subm_102',
        assignment=model.Assignment.query.filter_by(id=2).one(),
        user=model.User.query.filter_by(user_name='studente1').one(),
        language=model.Language.query.first())
    model.DBSession.add_all((subm_100, subm_101, subm_102))
    transaction.commit()

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
USERS = (                   None,       'studentc1','tutor1',    'teacher1',  'manager')
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
    (('/events/demo/admin', ['', '/', '/events', '/sheets', '/assignments', '/tests',
        '/newsitems', '/lessons', '/tutors', '/teams', '/students']),
                            401,        403,        403,        None),
    (('/events/demo/lessons/1', ['', '/',
        ('/submissions', ['', '/',
            ('/sheet/1', ['', '/assignment/1'])
        ])
    ]),
                            401,        403,        403,        None),
    (('/events/demo/lessons/2', ['', '/', '/lessons', '/tutors', '/teams', '/students']),
                            401,        403,        None),
    (('/events/demo/lessons/2', ['', '/',
        ('/submissions', ['', '/',
            ('/sheet/1', ['', '/assignment/1'])
        ])
    ]),
                            401,        403,        None),
    # A submission of studentc1, belonging to the lesson of tutor1
    (('/submissions/100', ['', '/', '/show', '/edit', '/result']),
                            401,        None,       None,       None,       None),
    ('/submissions/100/judge',
                            401,        403,        None),
    # Team member of studentc1 submission
    (('/submissions/101', ['', '/', '/show', '/result']),
                            401,        None),
    ('/submissions/101/edit',
                            401,        403,        None),
    # A submission of studente1, NOT belonging to the lesson of tutor1
    (('/submissions/102', ['', '/', '/show', '/edit', '/result', '/judge']),
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
                    _test_path.description = 'Site path %s for user %s returns HTTP status %s' % (p, user, status or '2xx or 3xx')
                    yield _test_path, p, user, status
