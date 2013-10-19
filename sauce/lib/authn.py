# -*- coding: utf-8 -*-
'''
@since: 05.04.2013

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

from zope.interface import implementer
from repoze.who.interfaces import IIdentifier, IMetadataProvider

import transaction
from sqlalchemy.orm.exc import NoResultFound


@implementer(IIdentifier)
class ExternalIdentifier(object):

    userid_key = 'repoze.who.userid'

    def __init__(self, remote_user_key='REMOTE_USER', remote_user_func=None, *args, **kw):
        self.remote_user_key = remote_user_key
        self.remote_user_func = remote_user_func

    #IIdentifier
    def identify(self, environ):
        if self.remote_user_key in environ and environ[self.remote_user_key]:
            value = environ[self.remote_user_key]
            if self.remote_user_func:
                value = self.remote_user_func(value)
            return {self.userid_key: unicode(value)}
        return None

    #IIdentifier
    def remember(self, environ, identity):
        return None

    #IIdentifier
    def forget(self, environ, identity):
        return None


@implementer(IMetadataProvider)
class ExternalMetadataProvider(object):

    userid_key = 'repoze.who.userid'

    def __init__(self, dbsession=None, user_class=None,
            metadata_mapping=[], *args, **kw):
        self.dbsession = dbsession
        self.user_class = user_class
        self.metadata_mapping = metadata_mapping

    #IMetadataProvider
    def add_metadata(self, environ, identity):
        #transaction.begin()
        with transaction.manager:
            user = identity.get('user', None)
            if not user:
                try:
                    user = self.dbsession.query(self.user_class).filter_by(user_name=identity[self.userid_key]).one()
                except NoResultFound:
                    user = self.user_class()
            for key, attr, func in self.metadata_mapping:
                value = environ.get(key)
                if func:
                    value = func(value)
                if getattr(user, attr) != value:
                    setattr(user, attr, value)
            self.dbsession.add(user)
#            print self.dbsession.new, self.dbsession.dirty, self.dbsession.deleted
            self.dbsession.flush()
        #transaction.commit()
        return


@implementer(IIdentifier, IMetadataProvider)
class ExternalAuth(ExternalIdentifier, ExternalMetadataProvider):

    def __init__(self, *args, **kw):
        ExternalIdentifier.__init__(self, *args, **kw)
        ExternalMetadataProvider.__init__(self, *args, **kw)
