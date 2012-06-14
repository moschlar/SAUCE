'''
Created on 14.06.2012

@author: moschlar
'''

from sauce.tests import TestController

__all__ = ['TestSite']


class TestSite(TestController):
    paths = ('', ['/', '/index', '/about', '/contact', '/login',
                ('/docs', ['', '/', '/tests', '/deutsch', '/tips', '/Changelog', '/Roadmap']),
                ('/events', ['', '/',
                    ('/eip12', ['/',
                        ('/sheets', ['', '/',
                            ('/1', ['', '/',
                                ('/assignments', ['', '/', '/1'])
                            ])
                        ])
                    ])
                ])
            ]
        )

    def _generate_paths(self, base=None):
        if base is None:
            base = self.paths
        a, b = base
        for c in b:
            if isinstance(c, tuple):
                for d in self._generate_paths(c):
                    yield a + d
            else:
                yield a + c

    def _test_path(self, path):
        response = self.app.get(path)
        assert response.status.startswith('2')

    def test_paths(self):
        for path in self._generate_paths():
            yield self._test_path, path
