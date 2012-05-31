# -*- coding: utf-8 -*-

"""The base Controller API.

@author: moschlar
"""

import logging

from tg import TGController, tmpl_context as c, url, request, abort
from tg.decorators import before_validate
from tg.i18n import ugettext as _, ungettext

import tw2.core as twc
import tw2.jquery as twj
import tw2.bootstrap as twb

import sauce.model as model
from sauce.model.event import Event

log = logging.getLogger(__name__)

__all__ = ['BaseController']

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

        # Set the correct originating url_scheme even if behind a proxy
        # The Apache config needs the following line to set this header:
        # RequestHeader set X_URL_SCHEME https
        environ['wsgi.url_scheme'] = environ.get('HTTP_X_URL_SCHEME', 'http')

        twj.jquery_js.no_inject = True
        twb.bootstrap_css.no_inject = True
        twb.bootstrap_js.no_inject = True
        twb.bootstrap_responsive_css.no_inject = True

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
            request.student = None
            request.teacher = None
            if isinstance(request.user, model.Student):
                request.student = request.user
            elif isinstance(request.user, model.Teacher):
                request.teacher = request.user
            c.user = request.user
            c.student = request.student
            c.teacher = request.teacher
        
        # Initialize other tmpl_context variables
        c.sub_menu = []
        c.side_menu = []
        
        # For the dropdown menu in navbar
        c.current_events = Event.current_events().all()
        c.future_events = Event.future_events().all()
        c.previous_events = Event.previous_events().all()
        c.events = set(c.current_events + c.future_events + c.previous_events)
        
        return super(BaseController, self).__call__(environ, start_response)

#        # Toscawidgets resource injection debugging
#        stream = TGController.__call__(self, environ, start_response)
#        local = twc.core.request_local()
#        log.debug(local)
#        return stream

@before_validate
def post(remainder, params):
    """Ensure that the decorated method is always called with POST."""
    if request.method.upper() == 'POST': return
    abort(405, headers=dict(Allow='POST'))
