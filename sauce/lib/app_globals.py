# -*- coding: utf-8 -*-
"""The application's Globals object

@author: moschlar
"""

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
        
        try:
            import pkg_resources
            dist = pkg_resources.get_distribution("SAUCE")
            self.version = u'%s' % dist.version
        except:
            self.version = u''
