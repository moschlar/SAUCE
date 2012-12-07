# -*- coding: utf-8 -*-
'''
Created on 12.11.2012

@author: moschlar
'''

import logging

import tw2.bootstrap.forms as twb

from sauce.model import NewsItem

from sauce.controllers.crc.base import FilteredCrudRestController

__all__ = ['NewsItemController']

log = logging.getLogger(__name__)


class NewsItemController(FilteredCrudRestController):

    model = NewsItem

    __table_options__ = {
        '__omit_fields__': ['event_id', 'user_id', 'user'],
        '__field_order__': ['id', 'date', 'subject', 'message', 'public'],
        'date': lambda filler, obj: obj.date.strftime('%c'),
        '__base_widget_args__': {'sortList': [[6, 0], [2, 0]]},
        }
    __form_options__ = {
        '__omit_fields__': ['id'],
        '__hide_fields__': ['user'],
        '__field_order__': ['id', 'date', 'event', 'subject', 'message', 'public'],
        '__field_widget_types__': {'subject': twb.TextField},
        '__field_widget_args__': {'date': {'date_format': '%d.%m.%Y %H:%M'},
                                  'event': {'help_text': u'If an event is set, the NewsItem will be shown on the event page; '
                                            'if no event is set, the NewsItem is shown on the news page'},
                                  },
        }
