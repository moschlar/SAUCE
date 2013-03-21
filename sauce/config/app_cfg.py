# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in SAUCE.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::

    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))

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

import locale
import logging

from tg import config
from tg.configuration import AppConfig
from routes.middleware import RoutesMiddleware
from beaker.middleware import CacheMiddleware

import sauce
from sauce import model
from sauce.lib import app_globals, helpers


log = logging.getLogger(__name__)


# Disable tw2 resource injection

#import tw2.core as twc
import tw2.jquery as twj
import tw2.bootstrap.forms as twbf

twj.jquery_js.no_inject = True
twbf.bootstrap_css.no_inject = True
twbf.bootstrap_js.no_inject = True
twbf.bootstrap_responsive_css.no_inject = True


class EnvironMiddleware(object):
    '''Middleware which updates the environ with a given dictionary

    This is useful for faking other middlewares which would change the
    environ dict in a way that is needed by other middlewares or the
    application.
    '''

    def __init__(self, app, config=None, d={}):
        self.app = app
        self.config = config
        self.d = d

    def __call__(self, environ, start_response):
        environ.update(self.d)
        return self.app(environ, start_response)


class SauceAppConfig(AppConfig):

    def __init__(self):
        super(SauceAppConfig, self).__init__()

        self.package = sauce

        self.default_renderer = 'mako'
        self.renderers = ['mako', 'json']

        self.use_toscawidgets = True  # For pygmentize...
        self.use_toscawidgets2 = True
        self.prefer_toscawidgets2 = True

        self.use_sqlalchemy = True
        self.model = model
        self.DBSession = model.DBSession

        # Handle other status codes, too
        self.handle_status_codes = [400, 403, 404, 405]

        # Only perform session.rollback(), not transaction.abort()
        self['tgext.crud.abort_transactions'] = False

        # Configure the authentication backend

        self.auth_backend = 'sqlalchemy'
        self.sa_auth.dbsession = model.DBSession

        # what is the class you want to use to search for users in the database
        self.sa_auth.user_class = model.User
        # what is the class you want to use to search for groups in the database
        self.sa_auth.group_class = model.Group
        # what is the class you want to use to search for permissions in the database
        self.sa_auth.permission_class = model.Permission

        # override this if you would like to provide a different who plugin for
        # managing login and logout of your application
        self.sa_auth.form_plugin = None

        # override this if you are using a different charset for the login form
        self.sa_auth.charset = 'utf-8'

        # You may optionally define a page where you want users to be redirected to
        # on login and logout:
        self.sa_auth.post_login_url = '/post_login'
        self.sa_auth.post_logout_url = '/post_logout'

    def add_core_middleware(self, app):
        '''Do not add beaker.SessionMiddleware but fake environ key for beaker.session'''
        app = RoutesMiddleware(app, config['routes.map'])
        # Disable the beaker SessionMiddleware
        #app = SessionMiddleware(app, config)
        # Insert the beaker.session key into environ
        app = EnvironMiddleware(app, config, {'beaker.session': False})
        app = CacheMiddleware(app, config)
        return app

    def after_init_config(self):
        if 'locale' in config:
            try:
                locale.setlocale(locale.LC_ALL, config.locale)
            except Exception as e:
                log.info('Could not set locale: %r' % e)


base_config = SauceAppConfig()
