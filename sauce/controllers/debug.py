# -*- coding: utf-8 -*-
"""Debug controller module"""
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

# turbogears imports
from tg import expose, request, url, TGController
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from repoze.what.predicates import has_permission
from pprint import pformat
from webhelpers.html import literal, escape

# project specific imports
#from sauce.lib.base import BaseController
#from sauce.model import DBSession, metadata


class DebugException(Exception):
    pass


class DebugController(TGController):

    allow_only = has_permission('manage')

    @expose('sauce.templates.page')
    def index(self, *args, **kwargs):
        content = literal(u'<h2></h2><ul>'
            '<li><a href="%(url)s/environ">request.environ</a></li>'
            '<li><a href="%(url)s/identity">request.identity</a></li>'
            '<li><a href="%(url)s/exception">DebugException</a></li>'
            '</ul>' % dict(url=url(self.mount_point)))
        return dict(page=u'debug', page_title=u'Debugging', page_header=u'Debugging', content=content)

    @expose('sauce.templates.page')
    def environ(self, *args, **kwargs):
        content = literal(u'<pre>') + escape(pformat(request.environ)) + literal(u'</pre>')
        return dict(page=u'debug', page_title=u'request.environ', page_header=u'request.environ', content=content)

    @expose('sauce.templates.page')
    def identity(self, *args, **kwargs):
        content = literal(u'<pre>') + escape(pformat(dict(request.environ.get('repoze.who.identity', dict()).items()))) + literal(u'</pre>')
        return dict(page=u'debug', page_title=u'request.identity', page_header=u'request.identity', content=content)

    @expose()
    def exception(self, *args, **kwargs):  # pragma: no cover
        raise DebugException(*args, **kwargs)
