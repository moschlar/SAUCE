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

import logging
import locale

from paste.deploy.converters import asbool

from tg import config  # @UnusedImport
from tg.util import Bunch
from tg.configuration import AppConfig

import sauce
from sauce import model
from sauce.lib import app_globals, helpers  # @UnusedImport
# from sauce.lib.authn import ExternalIdentifier, ExternalMetadataProvider


log = logging.getLogger(__name__)


# Disable tw2 resource injection

#import tw2.core as twc
import tw2.jquery as twj
import tw2.bootstrap.forms as twbf

twj.jquery_js.no_inject = True
twbf.bootstrap_css.no_inject = True
twbf.bootstrap_js.no_inject = True
twbf.bootstrap_responsive_css.no_inject = True


class EnvironMiddleware(object):  # pragma: no cover
    '''Middleware which updates the environ with a given dictionary

    This is useful for faking other middlewares which would change the
    environ dict in a way that is needed by other middlewares or the
    application.
    '''

    def __init__(self, app, config=None, d=None):
        self.app = app
        self.config = config
        self.d = d or dict()

    def __call__(self, environ, start_response):
        environ.update(self.d)
        return self.app(environ, start_response)


def add_sentry_middleware(app, error_middleware=False):
    '''Add Sentry middleware no matter what

    In full stack mode, it wraps just before the ErrorMiddleware,
    else it wraps in the after_config hook.
    '''
    from tg import config as tgconf
    fullstack = asbool(tgconf.get('fullstack'))
    if error_middleware or not fullstack:
        try:
            if tgconf.get('sentry.dsn', None):  # pragma: no cover
                from raven.contrib.pylons import Sentry as SentryMiddleware
                app = SentryMiddleware(app, tgconf)
        except ImportError:  # pragma: no cover
            pass
    return app


class SauceAppConfig(AppConfig):

    def __init__(self):
        super(SauceAppConfig, self).__init__()

        # Feature switches like http://code.flickr.net/2009/12/02/flipping-out/
        # Please note that all of the features here are off by default for a reason:
        # they are either highly specific to certain requirements or rarely tested
        self.features = {
            'externalauth': False,
            'lti': False,
        }

        self.package = sauce

        self.default_renderer = 'mako'
        self.renderers = ['mako', 'json']

        self.use_toscawidgets = False
        self.use_toscawidgets2 = True
        self.prefer_toscawidgets2 = True

        self.use_sqlalchemy = True
        self.model = model
        self.DBSession = model.DBSession

        self.register_hook('after_config', add_sentry_middleware)

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

        # External authentication support
        # uncomment and configure for your needs if needed

#         self.features['externalauth'] = True

        self.login = Bunch(url='/login', referrer_key='came_from', qualified=False)
        self.logout = Bunch(url='/logout_handler', referrer_key=None, qualified=False)

#        #self.sa_auth.remote_user_key = None
#        self.sa_auth.form_identifies = False
#
#        self.sa_auth.identifiers = [('externalid',
#            ExternalIdentifier(remote_user_key='HTTP_EPPN', remote_user_func=lambda v: v.split('@', 1)[0]))]
#        self.sa_auth.mdproviders = [('externalmd',
#            ExternalMetadataProvider(dbsession=model.DBSession, user_class=model.User,
#                metadata_mapping=[
#                    ('HTTP_EPPN', 'user_name', lambda v: v.split('@', 1)[0]),
#                    ('HTTP_DISPLAYNAME', 'display_name', None),
#                    ('HTTP_EPPN', 'email_address', lambda v: v.split('@', 1)[0] + '@example.com'),
#                ]))]

    def after_init_config(self):

        from tg import config as tgconf

        if tgconf.get('debug', False):
            # Always show warnings for the sauce module
            import warnings
            warnings.filterwarnings(action='once', module='sauce')
            warnings.filterwarnings(action='once', module='.*mak')

        _locale = tgconf.get('locale')

        try:
            locale.setlocale(locale.LC_ALL, _locale)
        except Exception:  # pragma: no cover
            log.exception('Could not set locale: %s' % _locale)
        else:
            log.info('Locale set to: %s' % _locale)

        for fmt in ('D_FMT', 'T_FMT', 'D_T_FMT'):
            fmtstr = tgconf.get(fmt, None)
            if fmtstr:
                # Self-baked %-escaping
                fmtstr = fmtstr.replace('%%', '%')
            if not fmtstr:
                fmtstr = locale.nl_langinfo(getattr(locale, fmt))
                log.info('Format string for %s read from locale: %s' % (fmt, fmtstr))
            setattr(tgconf, fmt, fmtstr)

    def add_error_middleware(self, global_conf, app):
        """Add middleware which handles errors and exceptions."""

        app = add_sentry_middleware(app, error_middleware=True)

        app = super(SauceAppConfig, self).add_error_middleware(global_conf, app)

        return app


base_config = SauceAppConfig()
