# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from sauce import model
from repoze.what import predicates
from sauce.model import DBSession, metadata
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from sauce.lib.base import BaseController
from sauce.lib.auth import is_enrolled
from sauce.controllers.error import ErrorController
from sauce.controllers.assignments import AssignmentsController
from sauce.controllers.submissions import SubmissionsController
from sauce.controllers.events import EventsController
from sauce.controllers.scores import ScoresController

from sauce.controllers.admin import MyAdminConfig
from sauce.controllers.news import NewsController

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
    
    @expose('sauce.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')
    
    @expose()
    def about(self):
        return dict(page='about')
    
    @expose()
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
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
