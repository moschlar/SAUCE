# -*- coding: utf-8 -*-
"""Main Controller

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
import logging

from tg import config, expose, flash, require, url, lurl, request, redirect, app_globals as g, abort, tmpl_context as c
from tg.decorators import paginate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.controller import AdminController

from docutils.core import publish_string
from webhelpers.html.tags import ul, link_to

from sauce import model
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, NewsItem, Event
from sauce.controllers.error import ErrorController
from sauce.controllers.submissions import SubmissionsController
from sauce.controllers.events import EventsController
from sauce.controllers.user import UserController
from sauce.controllers.language import LanguagesController
from sauce.controllers.debug import DebugController
from sauce.lib.menu import menu_docs
from sauce.config.admin import SAUCEAdminConfig

__all__ = ['RootController']

log = logging.getLogger(__name__)


class RootController(BaseController):
    """
    The root controller for the SAUCE application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    admin = AdminController(model, DBSession, SAUCEAdminConfig)

    error = ErrorController()

    # OUR CONTROLLERS
    #assignments = AssignmentsController()
    submissions = SubmissionsController()
    events = EventsController()
    #scores = ScoresController()
    user = UserController()
    languages = LanguagesController()

    debug = config.get('debug', False) and DebugController() or None

    @expose('sauce.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('sauce.templates.about')
    def about(self):
        c.side_menu = c.doc_menu
        return dict(page='about')

    @expose('sauce.templates.page')
    def docs(self, arg=''):
        page_title = u'SAUCE Documentation'
        page_header = u''

        if arg:
            try:
                f = open(os.path.join(g.loc, 'docs', arg + '.rst'))
            except IOError:
                abort(404)
            else:
                content = publish_string(f.read(), writer_name='html',
                    settings_overrides={'output_encoding': 'unicode'})
                page_title += ' - %s' % arg.capitalize()
        else:
            page_header = u'SAUCE Documentation'
            content = u'<p>In the menu on the left, you find all kinds of documentation about <b>SAUCE</b>.</p>'

        c.side_menu = c.doc_menu

        return dict(page='docs', page_title=page_title, page_header=page_header, content=content)

    @expose('sauce.templates.contact')
    def contact(self):
        return dict(page='contact')

    @expose('sauce.templates.news')
    @paginate('news', max_items_per_page=65535)
    def news(self):
        '''NewsItem listing page'''
        news_query = NewsItem.query.filter(NewsItem.event_id == None)

        if 'manage' not in request.permissions and \
            request.user not in ((e.teacher for e in Event.query)):
            news_query = news_query.filter_by(public=True)

        return dict(page='news', news=news_query)

    @expose('sauce.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        if request.environ.get('repoze.who.identity', None):
            # Already authenticated through external means or by manual URL access
            #TODO: Clear flash message cookie
            redirect(came_from)
        login_counter = request.environ.get('repoze.who.logins', 0)
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=unicode(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        user = request.user
        flash(_('Welcome back, %s!') % user.display_name)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
