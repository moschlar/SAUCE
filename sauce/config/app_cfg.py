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

from tg.configuration import AppConfig

import sauce
from sauce import model
from sauce.lib import app_globals, helpers

try:
    import locale
    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
except:
    pass

base_config = AppConfig()
base_config.renderers = []

base_config.prefer_toscawidgets2 = True
base_config.use_toscawidgets2 = True

base_config.package = sauce

#Enable json in expose
base_config.renderers.append('json')

#Enable genshi in expose to have a lingua franca for extensions and pluggable apps
#you can remove this if you don't plan to use it.
#base_config.renderers.append('genshi')

#Set the default renderer
base_config.default_renderer = 'mako'
base_config.renderers.append('mako')
#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = sauce.model
base_config.DBSession = sauce.model.DBSession
# Configure the authentication backend

# YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP
base_config.sa_auth.cookie_secret = "ChangeME"

base_config.auth_backend = 'sqlalchemy'
base_config.sa_auth.dbsession = model.DBSession

# what is the class you want to use to search for users in the database
base_config.sa_auth.user_class = model.User
# what is the class you want to use to search for groups in the database
base_config.sa_auth.group_class = model.Group
# what is the class you want to use to search for permissions in the database
base_config.sa_auth.permission_class = model.Permission

# override this if you would like to provide a different who plugin for
# managing login and logout of your application
base_config.sa_auth.form_plugin = None

# override this if you are using a different charset for the login form
base_config.sa_auth.charset = 'utf-8'

# You may optionally define a page where you want users to be redirected to
# on login:
base_config.sa_auth.post_login_url = '/post_login'

# You may optionally define a page where you want users to be redirected to
# on logout:
base_config.sa_auth.post_logout_url = '/post_logout'

# Handle other status codes, too
base_config.handle_status_codes = [400, 403, 404, 405]

# Only perform session.rollback(), not transaction.abort()
base_config['tgext.crud.abort_transactions'] = False

# Disable tw2 resource injection

import tw2.core as twc
import tw2.jquery as twj
import tw2.bootstrap.forms as twbf

twj.jquery_js.no_inject = True
twbf.bootstrap_css.no_inject = True
twbf.bootstrap_js.no_inject = True
twbf.bootstrap_responsive_css.no_inject = True
