# -*- coding: utf-8 -*-
"""WebHelpers used in SAUCE.

@author: moschlar
"""

from datetime import datetime

from tg import url as tgurl
#from webhelpers import date, feedgenerator, html, number, misc, text

import webhelpers as w

from webhelpers.html.tags import link_to
from webhelpers.text import truncate
from webhelpers.date import distance_of_time_in_words

from genshi.core import striptags

import re

#log = logging.getLogger(__name__)

cut = lambda text, max=200: truncate(text, max, whole_word=True)
strftimedelta = lambda delta, granularity='minute': distance_of_time_in_words(datetime.now(), datetime.now()+delta, granularity)
striphtml = striptags

def link(label, url='', **attrs):
    return link_to(label, tgurl(url), **attrs)


