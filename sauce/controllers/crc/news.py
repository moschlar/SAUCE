# -*- coding: utf-8 -*-
'''
Created on 12.11.2012

@author: moschlar
'''

import logging

#from tw2.forms import TextField, SingleSelectField, Label, TextArea, CheckBox
#from tw2.tinymce import TinyMCEWidget
#import tw2.core as twc
import tw2.tinymce as twt
import tw2.bootstrap.forms as twb
import tw2.jqplugins.chosen.widgets as twjc

from sauce.model import DBSession, NewsItem

from sauce.controllers.crc.base import FilteredCrudRestController

__all__ = ['NewsItemController']

log = logging.getLogger(__name__)


class NewsItemController(FilteredCrudRestController):

    model = NewsItem

    __table_options__ = {
        '__omit_fields__': ['event_id', 'user_id', 'user'],
        '__field_order__': ['id', 'date', 'subject', 'message', 'public'],
        'date': lambda filler, obj: obj.date.strftime('%x %X'),
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
