# -*- coding: utf-8 -*-
"""Error controller"""

import logging
from tg import request, expose

log = logging.getLogger(__name__)

__all__ = ['ErrorController']

messages = {400: u"<p>We're sorry, but you made an invalid request.</p>",
            403: u"<p>We're sorry, but you are not allowed to access "\
                "this page.</p>",
            404: u"<p>We're sorry, but the page you were trying to "\
                "access does not exist.</p>",
            405: u"<p>We're sorry, but the page you were trying to "\
                "access does not allow this method.</p>",
            500: u"<p>We're sorry, but an internal error occured while "\
                "processing your request.</p>"}
default_message = u"<p>We're sorry, but we weren't able to process "\
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
        code = request.params.get('code', resp.status_int)
        status = resp.status or code
        req = request.environ.get('pylons.original_request')

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
