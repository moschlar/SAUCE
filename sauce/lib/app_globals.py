# -*- coding: utf-8 -*-
"""The application's Globals object

@author: moschlar
"""

import os

__all__ = ['Globals']


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """

    def __init__(self):

        self.title = u'SAUCE'
        self.subtitle = u'System for AUtomated Code Evaluation'
        self.version = u''
        self.loc = '/'.join(os.path.dirname(__file__).split('/')[:-2])

        try:
            import pkg_resources
            dist = pkg_resources.get_distribution("SAUCE")
            self.version += u'%s ' % dist.version
            self.loc = dist.location
        except:
            pass

