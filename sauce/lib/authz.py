# -*- coding: utf-8 -*-
'''
@since: 18.03.2012

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

import logging

#TODO: Use environ instead of request if possible
from tg import request

from repoze.what.predicates import Predicate

log = logging.getLogger(__name__)


class user_is(Predicate):
    '''Generic request.user attribute equality checker class'''

    message = u'The user must be the %(attribute)s for this %(name)s'

    def __init__(self, attribute, obj, *args, **kwargs):
        self.attribute = attribute
        self.obj = obj
        self.name = self.obj.__class__.__name__
        super(user_is, self).__init__(*args, **kwargs)

    def evaluate(self, environ, credentials):
        if request.user and self.obj:
            attr = getattr(self.obj, self.attribute, None)
            if request.user == attr:
                return
        self.unmet()


class user_is_in(Predicate):
    '''Generic request.user attribute containment checker class'''

    message = u'The user must be a %(attribute)s for this %(name)s'

    def __init__(self, attribute, obj, *args, **kwargs):
        self.attribute = attribute
        self.obj = obj
        self.name = self.obj.__class__.__name__
        super(user_is_in, self).__init__(*args, **kwargs)

    def evaluate(self, environ, credentials):
        if request.user and self.obj:
            try:
                attr = getattr(self.obj, self.attribute, [])
                if request.user in attr:
                    return
            except:
                log.exception('')
        self.unmet()


class is_public(Predicate):
    '''Check if given object is public'''

    message = u'This %(name)s must be public'

    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        super(is_public, self).__init__(**kwargs)

    def evaluate(self, environ, credentials):
        if not getattr(self.obj, 'public', True):
            self.unmet()
        return

