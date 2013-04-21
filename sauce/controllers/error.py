# -*- coding: utf-8 -*-
"""Error controller"""
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
from tg import request, expose, redirect, url

log = logging.getLogger(__name__)

__all__ = ['ErrorController']

messages = {
    400: u"<p>We're sorry, but you made an invalid request.</p>",
    403: u"<p>We're sorry, but you are not allowed to access "
        "this page.</p>",
    404: u"<p>We're sorry, but the page you were trying to "
        "access does not exist.</p>",
    405: u"<p>We're sorry, but the page you were trying to "
        "access does not allow this method.</p>",
    500: u"<p>We're sorry, but an internal error occured while "
        "processing your request.</p>",
}
default_message = u"<p>We're sorry, but we weren't able to process " \
    "this request.</p>"


class ErrorController(object):
    """
    Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    @expose('sauce.templates.error')
    def document(self, *args, **kwargs):
        """Render the error document"""
        resp = request.environ.get('pylons.original_response')
        if not resp:
            log.info('ErrorDocument without original_response')
            redirect(url('/'))
        code = request.params.get('code', resp.status_int)
        status = resp.status or code

        req = request.environ.get('pylons.original_request')
        if not req:
            log.info('ErrorDocument without original_request')
            redirect(url('/'))

        log.info('Error %s, Request: %s %s, Referer: %s', status,
            req.method, req.url, req.referer)

        message = messages.get(code, default_message)
        if req.referer:
            message += ('<p><a href="%s" class="btn btn-inverse">'
                '<i class="icon-arrow-left icon-white"></i>'
                '&nbsp;Go back</a></p>' % req.referer)

        values = dict(prefix=request.environ.get('SCRIPT_NAME', ''),
            status=status, code=code,
            message=request.params.get('message', message))
        return values
