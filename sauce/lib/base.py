# -*- coding: utf-8 -*-

"""The base Controller API.

@author: moschlar
"""

import logging

from tg import TGController, tmpl_context as c, request, abort, lurl
from tg.decorators import before_validate
#from tg.i18n import ugettext as _, ungettext

# import tw2.core as twc

import sauce.model as model
from sauce.model.event import Event
from sauce.lib.menu import menu_docs, menu_events

log = logging.getLogger(__name__)

__all__ = ['BaseController']


def _allowance(obj):
    """Recursively gather teachers and tutors from the object hierarchy
    and check if request.user is a member"""
    users = set()
    while obj:
        for group in ('teachers', 'tutors'):
            users |= set(getattr(obj, group, []))
        for user in ('teacher', 'tutor'):
            u = getattr(obj, user, False)
            if u:
                users |= set((u, ))
        obj = obj.parent
    return 'manage' in request.permissions or request.user in users


class BaseController(TGController):
    """
    Base class for the controllers in the application.

    Your web application should have one of these. The root of
    your application is used to compute URLs used by your app.

    """

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # TGController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']

        # Fill tmpl_context with user data for convenience
        request.identity = c.identity = environ.get('repoze.who.identity')

        try:
            request.user = request.identity.get('user')
        except:
            request.user = None
        finally:
            try:
                request.permissions = request.identity.get('permissions')
            except AttributeError:
                request.permissions = []
            request.student = request.user
            request.teacher = request.user
            c.user = request.user
            c.student = request.user
            c.teacher = request.user

        request.referer = request.environ.get('HTTP_REFERER', None)

        request.allowance = _allowance

        # Initialize other tmpl_context variables
        c.sub_menu = []
        c.side_menu = []

        doc_list = list([('About', lurl('/about'), 'info-sign'), None] +
            list((label, lurl('/docs/' + url), 'book') for label, url in (
                ('Changelog', 'Changelog'), ('Roadmap', 'Roadmap'),
                ('Deutsche Dokumentation', 'deutsch'), ('Test configuration', 'tests'),
                ('Tips and Tricks', 'tips')
            )) + [None, ('Language information', '/languages', 'list-alt')])

        c.doc_menu = menu_docs(doc_list)

        c.event_menu = menu_events(Event.current_events(), Event.future_events(), Event.previous_events())

        return super(BaseController, self).__call__(environ, start_response)

        # # Toscawidgets resource injection debugging
        # stream = TGController.__call__(self, environ, start_response)
        # local = twc.core.request_local()
        # log.debug(local)
        # return stream

@before_validate
def post(remainder, params):
    """Ensure that the decorated method is always called with POST."""
    if request.method.upper() == 'POST': return
    abort(405, headers=dict(Allow='POST'))
