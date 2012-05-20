# -*- coding: utf-8 -*-
"""Main Controller

@author: moschlar
"""
import os

from tg import expose, flash, require, url, lurl, request, redirect, app_globals as g, abort
from tg.i18n import ugettext as _, lazy_ugettext as l_
from sauce import model
from repoze.what import predicates
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from docutils.core import publish_string
from webhelpers.html.tags import ul, link_to

from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata
from sauce.controllers.error import ErrorController
from sauce.controllers.assignments import AssignmentsController
from sauce.controllers.submissions import SubmissionsController
from sauce.controllers.events import EventsController
from sauce.controllers.scores import ScoresController

from sauce.controllers.admin import MyAdminConfig
from sauce.controllers.news import NewsController
from sauce.controllers.user import UserController


__all__ = ['RootController']


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
    admin = AdminController(model, DBSession, config_type=MyAdminConfig)
    
    error = ErrorController()
    
    # OUR CONTROLLERS
    #assignments = AssignmentsController()
    submissions = SubmissionsController()
    events = EventsController()
    #scores = ScoresController()
    #tests = TestsController()
    news = NewsController()
    user = UserController()
    
    @expose('sauce.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')
    
    @expose('sauce.templates.about')
    def about(self):
        return dict(page='about')
    
    @expose('sauce.templates.docs')
    def docs(self, arg=''):
        if arg:
            try:
                f = open(os.path.join(g.loc, 'docs', arg+'.rst'))
            except IOError:
                abort(404)
            else:
                content = publish_string(f.read(), writer_name='html', settings_overrides={'output_encoding': 'unicode'})
        else:
            content = ul((link_to(label, lurl('/docs/' + url)) for label, url in
                          (('Changelog', 'Changelog'), ('Roadmap', 'Roadmap'),
                           ('Deutsche Dokumentation', 'deutsch'), ('Test configuration', 'tests'),
                           ('Tips and Tricks', 'tips'))))
        return dict(page='docs', heading=u'%s documentation' % arg.capitalize(), content=content)
    
    @expose('sauce.templates.contact')
    def contact(self):
        return dict(page='contact')
    
    @expose('sauce.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
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
