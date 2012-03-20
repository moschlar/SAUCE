# -*- coding: utf-8 -*-

"""WebHelpers used in SAUCE."""

from webhelpers import date, feedgenerator, html, number, misc, text

import re, logging

log = logging.getLogger(__name__)

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
    return re.sub('<[^<]+?>', '', text)

