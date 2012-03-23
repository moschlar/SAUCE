# -*- coding: utf-8 -*-
"""WebHelpers used in SAUCE."""

from webhelpers import date, feedgenerator, html, number, misc, text

import re, textwrap

#log = logging.getLogger(__name__)

# shortcut for links
link = html.tags.link_to

def strftimedelta(delta, format='%D Days %hh:%mm:%ss'):
    '''Return a string representing the timedelta element.
    
    Possible format codes are:
        %D days
        %h hours
        %hh hours with leading zero
        %m minutes
        %mm minutes with leading zero
        %s seconds
        %ss seconds with leading zero
    '''
    totalSeconds = delta.seconds
    hours, remainder = divmod(totalSeconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    result = format.replace('%D', str(delta.days)).\
            replace('%hh', '%2d' % hours).replace('%mm', '%2d' % minutes).\
            replace('%ss', '%2d' % seconds).\
            replace('%h', str(hours)).replace('%m', str(minutes)).\
            replace('%s', str(seconds))
    return result

def striphtml(text):
    return re.sub('<[^<]+?>', ' ', text).strip()

def cut(text):
    if len(text) < 200:
        return text
    else:
        return textwrap.wrap(text, 200)[0] + ' ...'