'''
Created on 14.06.2012

@author: moschlar
'''

from sauce.tests import TestController

# The USERS and PATHS variables are interpreted in a matrix-like style
# USERS contain valid usernames for the REMOTE_USER variable.
# The usernames should be sorted hierarchically to make configuration
# simpler
# PATHS contains a path and expected statuses for the above usernames.
# (statuses that are not specified aren't tested, of course)
# If path[0] is a tuple or list, it will be used for recursive url generation

#   PATH                    ANONYMOUS   STUDENT     TEACHERASS  TEACHER     MANAGER
USERS = (                   None,       'studenta1','teacherass','teacher','manager')
PATHS = (
    # All the static pages
    (('', ['/', '/index', '/about', '/contact', '/login',
        ('/docs', ['', '/', '/tests', '/deutsch', '/tips', '/Changelog', '/Roadmap'])
    ]),
                            None),
    # The basic event-sheet-assignment pages
    (('/events', ['', '/',
        ('/eip12', ['/',
            ('/sheets', ['', '/',
                ('/1', ['', '/',
                    ('/assignments', ['', '/', '/1'])
                ])
            ])
        ])
    ]),
                            None),
    (('/events/eip12/sheets/1/assignments/1/similarity', ['', '/dendrogram', '/dendrogram.png']),
                            401,        403,        None),
    ('/user',               401,        None),
    ('/admin',              401,        403,        403,        403,        None),
    ('/events/eip12/admin', 401,        403,        403,        None),
    (('/events/eip12/lessons/1', ['', '/',
        ('/submissions', ['', '/',
            ('/sheet/1', ['', '/assignment/1'])
        ])
    ]),
                            401,        403,        None),
    (('/events/eip12/lessons/2', ['', '/',
        ('/submissions', ['', '/',
            ('/sheet/1', ['', '/assignment/1'])
        ])
    ]),
                            401,        403,        403,        None),
    # WARNING: Submission ids come from websetup/data/course.py
    # A submission of studenta1, belonging to the lesson of teacherass
    (('/submissions/25', ['', '/', '/show', '/edit', '/result']),
                            401,        None,       None,       None,       None),
    ('/submissions/25/judge',
                            401,        403,        None),
    # Team member of studenta1 submission
    (('/submissions/26', ['', '/', '/show', '/result']),
                            401,        None),
    ('/submissions/26/edit',
                            401,        403,        None),
    # A submission of studentc1, NOT belonging to the lesson of teacherass
    (('/submissions/27', ['', '/', '/show', '/edit', '/result', '/judge']),
                            401,        403,        403,        None,       None),
    )


class TestSite(TestController):

    def _generate_paths(self, base):
        a, b = base
        for c in b:
            if isinstance(c, tuple):
                for d in self._generate_paths(c):
                    yield a + d
            else:
                yield a + c

    def _test_path(self, path, user=None, status=None):
        if user:
            env = dict(REMOTE_USER=user)
        else:
            env = None
        self.app.get(path, extra_environ=env, status=status)

    def test_paths(self):
        for path in PATHS:
            p, stati = path[0], path[1:]

            if isinstance(p, tuple):
                pp = self._generate_paths(p)
            else:
                pp = (p, )

            for p in pp:
                for i, status in enumerate(stati):
                    if status is not False:
                        user = USERS[i]
                        yield self._test_path, p, user, status

