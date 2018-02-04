'''
@since: 14.06.2012

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

import transaction

from sauce.tests import load_app, setup_app, teardown_db
from sauce import model


__all__ = ['test_paths']

app = None
''':type app: webtest.TestApp'''


def setUpModule():
    global app
    app = load_app()
    setup_app()

    # Prepare authz test data
    subm_100 = model.Submission(id=100, filename=u'subm_100', source=u'subm_100',
        assignment=model.Assignment.query.filter_by(id=2).one(),
        user=model.User.query.filter_by(user_name='studentc1').one(),
        language=model.Language.query.first(),
        judgement=model.Judgement(
            tutor=model.User.query.filter_by(user_name='tutor1').one(),
            corrected_source=u'subm-100', comment=u'Good good',
            annotations={1: 'No no no'}, grade=3.14))
    model.DBSession.add(subm_100)
    subm_101 = model.Submission(id=101, filename=u'subm_101', source=u'subm_101',
        assignment=model.Assignment.query.filter_by(id=2).one(),
        user=model.User.query.filter_by(user_name='studentc2').one(),
        language=model.Language.query.first())
    model.DBSession.add(subm_101)
    subm_102 = model.Submission(id=102, filename=u'subm_102', source=u'subm_102',
        assignment=model.Assignment.query.filter_by(id=2).one(),
        user=model.User.query.filter_by(user_name='studente1').one(),
        language=model.Language.query.first())
    model.DBSession.add(subm_102)
    subm_103 = model.Submission(id=103, filename=u'subm_103', source=u'subm_103',
        assignment=model.Assignment.query.filter_by(id=2).one(),
        user=model.User.query.filter_by(user_name='studente1').one(),
        language=model.Language.query.first(),
        public=True)
    model.DBSession.add(subm_103)
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
    (('', ['/', '/index', '/news', '/about', '/contact', '/login',
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
                            None,       None),
    (('/events/demo/sheets/1/assignments/1/similarity',
        ['', '/', '/table', '/list',
#                                     '/dendrogram', '/dendrogram.png',
        ]),                 401,        403,        None),
    ('/events/demo/sheets/1/assignments/1/submit',
                            401,        None),
    (('/user', ['', '/', '/profile']),
                            401,        None),
    ('/submissions',        401,        None),
    (('/admin', ['', '/', '/users', '/groups', '/permissions',
        '/events', '/ltis', '/languages', '/compilers', '/interpreters']),
                            401,        403,        403,        403,        None),
    (('/debug', ['', '/', '/environ', '/identity']),
                            401,        403,        403,        403,        None),
    (('/events/demo/admin', ['', '/',
        '/events', '/newsitems', '/lessons', '/tutors',
        '/teams', '/teams/rename', '/teams/1/rename',
        '/students', '/students?id=6', '/students?user_name=a1',
        '/students/new', '/students/6/edit', '/students/6/password',
        '/sheets', '/sheets/2/test',
        '/assignments', '/assignments/2/test',
        '/tests', '/tests/2/test',
    ]),
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
            ('/sheet/1', ['', '/assignment/1', '/assignment/0']), '/sheet/0',
            '/lesson/1', '/lesson/0', '/team/1', '/team/0',
        ])
    ]),
                            401,        403,        None),
    (('/events/demo', ['/submissions', '/submissions/user/6', '/submissions/user/0',
        '/sheets/1/submissions', '/sheets/1/assignments/1/submissions']),
                            401,        403,        403,        None),
    # A submission of studentc1, belonging to the lesson of tutor1
    (('/submissions/100', ['', '/', '/show', '/edit', '/result', '/clone',
        '/download', '/download/judgement', '/source', '/source/judgement']),
                            401,        None,       None,       None,       None),
    ('/submissions/100/judge',
                            401,        403,        None),
    ('/submissions/101/edit_',
                            401,        405),
    # Team member of studentc1 submission
    (('/submissions/101', ['', '/', '/show', '/result', '/download', '/download/judgement',
        '/source', '/source/judgement']),
                            401,        None),
    ('/submissions/101/edit',
                            401,        403,        None),
    # A submission of studente1, NOT belonging to the lesson of tutor1
    (('/submissions/102', ['', '/', '/show', '/edit', '/result', '/judge']),
                            401,        403,        403,        None,       None),
    (('/submissions/103', ['', '/', '/show', '/result', '/clone']),
                            401,        None,       None,       None,       None),
    (('/submissions/103', ['/edit', '/judge']),
                            401,        403,        None,       None,       None),  # TODO: tutor1 should not be able to edit and judge
    # _lookup error pages
    (('', ['/languages/0', '/events/0',
        '/events/demo/sheets/0', '/events/demo/sheets/1/assignments/0']),
                            404,        404),
    (('', ['/languages/abc',
        '/events/demo/sheets/abc', '/events/demo/sheets/1/assignments/abc']),
                            400,        400),
    ('/submissions/0',      401,        404),
    ('/submissions/abc',    401,        400),
    ('/events/demo/lessons/0',
                            401,        403,        404),
    ('/events/demo/lessons/abc',
                            401,        403,        400),

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
                    #_test_path.description = 'Site path %s for user %s returns HTTP status %s' % (p, user, status or '2xx or 3xx')
                    yield _test_path, p, user, status
