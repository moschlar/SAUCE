# -*- coding: utf-8 -*-
"""WebHelpers used in SAUCE.

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

import re
from datetime import datetime
from markupsafe import Markup
from pprint import pformat

from webhelpers import date, feedgenerator, html, number, misc, text
from webhelpers.html.tags import link_to, link_to_unless
from webhelpers.html.tools import mail_to
from webhelpers.text import truncate
from webhelpers.date import distance_of_time_in_words

from difflib import unified_diff

from tg import config, request, url as tgurl

from .sanitize import bleach_basic, bleach_simple, bleach_advanced

#log = logging.getLogger(__name__)


#----------------------------------------------------------------------


cut = lambda text, max = 200: truncate(text, max, whole_word=True)


def link(label, url='', **attrs):
    return link_to(label, tgurl(url), **attrs)


def striphtml(text):
    return re.sub('<[^<]+?>', ' ', text).strip() if text else u''


def icon(icon_name, white=False):
    if (white):
        return html.literal('<i class="icon-%s icon-white"></i>' % icon_name)
    else:
        return html.literal('<i class="icon-%s"></i>' % icon_name)

def icon(icon_name):
    return Markup('<i class="glyphicon glyphicon-%s"></i>' % icon_name)

#----------------------------------------------------------------------


def current_year():
    now = datetime.now()
    return now.strftime('%Y')


def strftime(x, human=False):
    if x:
        if human:
            return x.strftime('%c').decode('utf-8')
        else:
            return x.strftime(config.D_T_FMT)
    else:
        return u''


strftimedelta = (lambda delta, granularity='minute':
    distance_of_time_in_words(datetime.now(), datetime.now() + delta, granularity))


#----------------------------------------------------------------------


def udiff(a, b, a_name=None, b_name=None, **kw):
    '''Automatically perform splitlines on a and b before diffing and join output'''
    if not a:
        a = u''
    if not b:
        b = u''
    return '\n'.join(unified_diff(a.splitlines(), b.splitlines(),
        a_name, b_name, lineterm='', **kw))


#----------------------------------------------------------------------


def make_login_url():
    url = '/login'
    params = {'came_from': request.environ['PATH_INFO']}
    qualified = False
    try:
        url = config.login.url
        qualified = config.login.qualified
        if config.login.referrer_key:
            params = {config.login.referrer_key: tgurl(request.environ['PATH_INFO'], qualified=qualified)}
    except:  # pragma: no cover
        pass
    return tgurl(url, params)


def make_logout_url():
    url = '/logout_handler'
    params = {}
    qualified = False
    try:
        url = config.logout.url
        qualified = config.logout.qualified
        if config.logout.referrer_key:
            params = {config.logout.referrer_key: tgurl(request.environ['PATH_INFO'], qualified=qualified)}
    except:  # pragma: no cover
        pass
    return tgurl(url, params=params)
