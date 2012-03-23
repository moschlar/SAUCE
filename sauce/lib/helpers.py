# -*- coding: utf-8 -*-

"""WebHelpers used in SAUCE."""

from webhelpers import date, feedgenerator, html, number, misc, text

import re, textwrap

#log = logging.getLogger(__name__)

# shortcut
link = html.tags.link_to

def strftimedelta(delta, format='%D Days %H:%M:%S'):
    
    totalSeconds = delta.seconds
    hours, remainder = divmod(totalSeconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    result = format.replace('%D', str(delta.days)).replace('%H', str(hours)).\
            replace('%M', str(minutes)).replace('%S', str(seconds))
    return result

def striphtml(text):
    return re.sub('<[^<]+?>', ' ', text)

def cut(text):
    if len(text) < 200:
        return text
    else:
        return textwrap.wrap(text, 200)[0] + ' ...'