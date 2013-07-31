# -*- coding: utf-8 -*-
"""Fallback controller."""
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

from sauce.lib.base import BaseController
from tg import abort

__all__ = ['TemplateController']


class TemplateController(BaseController):
    """
    The fallback controller for SAUCE.

    By default, the final controller tried to fulfill the request
    when no other routes match. It may be used to display a template
    when all else fails, e.g.::

        def view(self, url):
            return render('/%s' % url)

    Or if you're using Mako and want to explicitly send a 404 (Not
    Found) response code when the requested template doesn't exist::

        import mako.exceptions

        def view(self, url):
            try:
                return render('/%s' % url)
            except mako.exceptions.TopLevelLookupException:
                abort(404)

    """

    def view(self, url):
        """Abort the request with a 404 HTTP status code."""
        abort(404)
