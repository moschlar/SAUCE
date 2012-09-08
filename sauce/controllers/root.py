# -*- coding: utf-8 -*-
"""Main Controller

@author: moschlar
"""
import os

from tg import expose, flash, require, url, lurl, request, redirect, app_globals as g, abort, tmpl_context as c
from tg.decorators import paginate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.controller import AdminController

from docutils.core import publish_string
from webhelpers.html.tags import ul, link_to

from sauce import model
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, NewsItem
from sauce.controllers.error import ErrorController
from sauce.controllers.submissions import SubmissionsController
from sauce.controllers.events import EventsController
from sauce.controllers.user import UserController
from sauce.controllers.similarity import SimilarityController
from sauce.lib.menu import menu_list


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
    admin = AdminController(model, DBSession)

    error = ErrorController()

    # OUR CONTROLLERS
    #assignments = AssignmentsController()
    submissions = SubmissionsController()
    events = EventsController()
    #scores = ScoresController()
    user = UserController()

    #Testing
    #similarity = SimilarityController()

    @expose('sauce.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('sauce.templates.about')
    def about(self):
        return dict(page='about')

    @expose('sauce.templates.page')
    def docs(self, arg=''):
        heading = u'SAUCE Documentation'
        doc_list = list((label, lurl('/docs/' + url)) for label, url in
                    (('Changelog', 'Changelog'), ('Roadmap', 'Roadmap'),
                    ('Deutsche Dokumentation', 'deutsch'), ('Test configuration', 'tests'),
                    ('Tips and Tricks', 'tips')))
        if arg:
            try:
                f = open(os.path.join(g.loc, 'docs', arg + '.rst'))
            except IOError:
                abort(404)
            else:
                content = publish_string(f.read(), writer_name='html',
                    settings_overrides={'output_encoding': 'unicode'})
                heading += ' - %s' % arg.capitalize()
        else:
            content = ul((link_to(label, url) for label, url in doc_list))

        c.side_menu = menu_list(doc_list, icon_name='book')

        return dict(page='docs', heading=heading, content=content)

    @expose('sauce.templates.contact')
    def contact(self):
        return dict(page='contact')

    @paginate('news')
    @expose('sauce.templates.news')
    def news(self, page=1):
        '''NewsItem listing page'''

        news_query = NewsItem.query.filter(NewsItem.event_id == None)
        if not request.teacher:
            news_query = news_query.filter_by(public=True)

        #news = Page(news_query, page=page, items_per_page=20)

        return dict(page='news', news=news_query)

    @expose('sauce.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
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
