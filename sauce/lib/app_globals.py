# -*- coding: utf-8 -*-
"""The application's Globals object

@author: moschlar
"""

import os
from tg import lurl

__all__ = ['Globals']


class Globals(object):
    """Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the 'app_globals' variable.

    """

    def __init__(self):

        self.title = u'SAUCE'
        self.subtitle = u'System for AUtomated Code Evaluation'
        self.loc = '/'.join(os.path.dirname(__file__).split('/')[:-2])

        try:
            import pkg_resources
            dist = pkg_resources.get_distribution("SAUCE")
            self.loc = dist.location
            self.version = u'%s' % dist.version
        except:
            self.version = u''

        try:
            from subprocess import check_output
            self.revision = check_output('cd %s && git describe --tags' % self.loc, shell=True).strip()
        except:
            self.revision = u''

        self.doc_list = list((label, lurl('/docs/' + url)) for label, url in
                    (('Changelog', 'Changelog'), ('Roadmap', 'Roadmap'),
                    ('Deutsche Dokumentation', 'deutsch'), ('Test configuration', 'tests'),
                    ('Tips and Tricks', 'tips')))
