# -*- coding: utf-8 -*-
"""The application's Globals object

@author: moschlar
"""

from webhelpers.html import literal

__all__ = ['Globals']

class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """

    def __init__(self):
        """Do nothing, by default."""
        self.title = u'SAUCE'
        self.subtitle = u'System for AUtomated Code Evaluation'
        self.version = u''
        
        try:
            import pkg_resources
            dist = pkg_resources.get_distribution("SAUCE")
            self.version += u'%s ' % dist.version
            loc = dist.location
        except:
            pass
        
        if 'dev' in self.version:
            try:
                from dulwich.repo import Repo
                h = Repo(loc).head()
                github_url_commit = 'https://github.com/moschlar/SAUCE/commit/'
                self.version += u'- <a href="'+github_url_commit+'%s">rev %s</a>'  % (h, h[:7])
                self.version = literal(self.version)
            except:
                pass
