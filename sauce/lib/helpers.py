# -*- coding: utf-8 -*-

"""WebHelpers used in SAUCE.

@author: moschlar
"""

from datetime import datetime

from tg import url as tgurl

from webhelpers import date, feedgenerator, html, number, misc, text
from webhelpers.html.tags import link_to, link_to_unless
from webhelpers.html.tools import mail_to
from webhelpers.text import truncate
from webhelpers.date import distance_of_time_in_words

import re

from pygments import highlight as _highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from difflib import unified_diff

#log = logging.getLogger(__name__)

cut = lambda text, max=200: truncate(text, max, whole_word=True)
strftimedelta = lambda delta, granularity='minute': distance_of_time_in_words(datetime.now(), datetime.now()+delta, granularity)

#----------------------------------------------------------------------

def link(label, url='', **attrs):
    return link_to(label, tgurl(url), **attrs)

def striphtml(text):
    return re.sub('<[^<]+?>', ' ', text).strip() if text else u''

def current_year():
  now = datetime.now()
  return now.strftime('%Y')

def icon(icon_name, white=False):
    if (white):
        return html.literal('<i class="icon-%s icon-white"></i>' % icon_name)
    else:
        return html.literal('<i class="icon-%s"></i>' % icon_name)

#----------------------------------------------------------------------

class MyHtmlFormatter(HtmlFormatter):
    '''Create lines that have unique name tags to allow highlighting
    
    Each line has an anchor named <lineanchors>-<linenumber>
    '''
    
    def _wrap_lineanchors(self, inner):
        s = self.lineanchors
        i = 0
        for t, line in inner:
            if t:
                i += 1
                yield 1, '<a name="%s-%d" class="%s-%d"">%s</a>' % (s, i, s, i, line)
            else:
                yield 0, line

formatter = MyHtmlFormatter(style='default', linenos=True, lineanchors='line')
style = formatter.get_style_defs()

def udiff(a, b, a_name=None, b_name=None, **kw):
    '''Automatically perform splitlines on a and b before diffing and join output'''
    if not a: a=u''
    if not b: b=u''
    return '\n'.join(unified_diff(a.splitlines(), b.splitlines(), a_name, b_name, lineterm='', **kw))

def highlight(code, lexer_name):
    #formatter = MyHtmlFormatter(style='default', linenos=True, lineanchors='line')
    if code:
        return _highlight(code, get_lexer_by_name(lexer_name), formatter)
    else:
        return u''

