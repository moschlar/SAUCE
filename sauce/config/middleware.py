# -*- coding: utf-8 -*-
"""WSGI middleware initialization for the SAUCE application."""
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

from sauce.config.app_cfg import base_config
from sauce.config.environment import load_environment


__all__ = ['make_app']

log = logging.getLogger(__name__)

# Use base_config to setup the necessary PasteDeploy application factory.
# make_base_app will wrap the TG2 app with all the middleware it needs.
make_base_app = base_config.setup_tg_wsgi_app(load_environment)


class MyMiddleware(object):
    '''WSGI Middleware wrapper'''

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def __call__(self, environ, response):
        # Set the correct originating url_scheme even if behind a proxy
        # The Apache config needs the following line to set this header:
        # RequestHeader set X_FORWARDED_PROTO https
        environ['wsgi.url_scheme'] = environ.get('HTTP_X_FORWARDED_PROTO', 'http')
        return self.app(environ, response)


def make_app(global_conf, full_stack=True, **app_conf):
    """
    Set SAUCE up with the settings found in the PasteDeploy configuration
    file used.

    :param global_conf: The global settings for SAUCE (those
        defined under the ``[DEFAULT]`` section).
    :type global_conf: dict
    :param full_stack: Should the whole TG2 stack be set up?
    :type full_stack: str or bool
    :return: The SAUCE application with all the relevant middleware
        loaded.

    This is the PasteDeploy factory for the SAUCE application.

    ``app_conf`` contains all the application-specific settings (those defined
    under ``[app:main]``.
    """
    app = make_base_app(global_conf, full_stack=True, **app_conf)

    # Wrap your base TurboGears 2 application with custom middleware here

    app = MyMiddleware(app)

    return app
