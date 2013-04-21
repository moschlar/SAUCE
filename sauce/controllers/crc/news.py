# -*- coding: utf-8 -*-
'''
Created on 12.11.2012

@author: moschlar
'''
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

import logging

import tw2.bootstrap.forms as twb
import tw2.tinymce as twt

from sauce.model import NewsItem

from sauce.controllers.crc.base import FilterCrudRestController

__all__ = ['NewsItemController']

log = logging.getLogger(__name__)


class NewsItemController(FilterCrudRestController):

    model = NewsItem

    __table_options__ = {
        '__omit_fields__': ['event_id', 'user_id', 'user'],
        '__field_order__': ['id', 'date', 'subject', 'message', 'public'],
        'date': lambda filler, obj: \
            obj.date.strftime('%c'),
        '__base_widget_args__': {'sortList': [[6, 0], [2, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': ['id'],
        '__hide_fields__': ['user'],
        '__field_order__': ['id', 'date', 'event', 'subject', 'message', 'public'],
        '__field_widget_types__': {'subject': twb.TextField, 'message': twt.TinyMCEWidget},
        '__field_widget_args__': {
            'subject': {'css_class': 'span4'},
            'message': {'css_class': 'span7'},
            'date': {'date_format': '%d.%m.%Y %H:%M'},
            'event': {'help_text': u'''
If an event is set, the NewsItem will be shown on the event page; 
if no event is set, the NewsItem is shown on the news page'''},
        },
    }
