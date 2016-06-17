# -*- coding: utf-8 -*-
"""The base Controller API.

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

import logging

from tg import TGController, tmpl_context as c, request, abort, lurl
from tg.decorators import before_validate
#from tg.i18n import ugettext as _, ungettext

import status

# import tw2.core as twc

import sauce.model as model
from sauce.model.event import Event
from sauce.lib.menu import menu_docs, menu_events

log = logging.getLogger(__name__)

__all__ = ['BaseController']


def _allowance(obj):
    """Recursively get teachers and tutors from the object hierarchy
    and check if request.user is a member"""
    if request.user:
        if 'manage' in request.permissions:
            return True
        try:
            while obj:
                for group in ('teachers', 'tutors'):
                    if request.user in getattr(obj, group, []):
                        return True
                for user in ('teacher', 'tutor'):
                    if request.user is getattr(obj, user, None):
                        return True
                obj = obj.parent
        except:
            pass
    return False


class BaseController(TGController):
    """
    Base class for the controllers in the application.

    Your web application should have one of these. The root of
    your application is used to compute URLs used by your app.

    """

    def __call__(self, environ, context):
        """Invoke the Controller"""
        # TGController.__call__ dispatches to the Controller method
        # the request is routed to.

        # Fill tmpl_context with user data for convenience
        request.identity = c.identity = environ.get('repoze.who.identity')

        try:
            request.user = model.DBSession.merge(request.identity.get('user'))
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
                ('Changelog', 'Changelog'),
                ('Roadmap', 'Roadmap'),
                ('Deutsche Dokumentation', 'deutsch'),
                ('Tips and Tricks', 'tips'),
                ('Test configuration', 'tests'),
            )) + [None, ('Language information', '/languages', 'list-alt')])

        c.doc_menu = menu_docs(doc_list)

        c.event_menu = menu_events(Event.current_events(), Event.future_events(), Event.previous_events())

        return super(BaseController, self).__call__(environ, context)

        # # Toscawidgets resource injection debugging
        # stream = TGController.__call__(self, environ, context)
        # local = twc.core.request_local()
        # log.debug(local)
        # return stream


@before_validate
def post(remainder, params):
    """Ensure that the decorated method is always called with POST."""
    if request.method.upper() == 'POST':
        return
    abort(status.HTTP_405_METHOD_NOT_ALLOWED, headers=dict(Allow='POST'))
