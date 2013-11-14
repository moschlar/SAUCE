# -*- coding: utf-8 -*-
"""The application's Globals object

@author: moschlar
"""
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
        except:  # pragma: no cover
            self.version = u''

        try:
            from subprocess import check_output
            self.revision = check_output('cd %s && git describe --tags' % self.loc, shell=True).strip()
        except:  # pragma: no cover
            self.revision = u''
