# -*- coding: utf-8 -*-
'''CrudControllers for NewsItem entities

@since: 12.11.2012

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

from sauce.controllers.crc.base import FilterCrudRestController
from sauce.model import NewsItem
import sauce.lib.helpers as h

import logging
log = logging.getLogger(__name__)

__all__ = ['NewsItemController']


class NewsItemController(FilterCrudRestController):
    '''CrudController for News'''

    model = NewsItem

    __table_options__ = {
        '__omit_fields__': ['event_id', 'user_id', 'user'],
        '__field_order__': ['id', 'date', 'subject', 'message', 'public'],
        'date': lambda filler, obj: h.strftime(obj.date, False),
        '__base_widget_args__': {'sortList': [[6, 0], [2, 0]]},
    }
    __form_options__ = {
        '__omit_fields__': ['id'],
        '__hide_fields__': ['user'],
        '__field_order__': ['id', 'date', 'event', 'subject', 'message', 'public'],
        '__field_widget_args__': {
            'event': {
                'help_text': u'''
If an event is set, the NewsItem will be shown on the event page; 
if no event is set, the NewsItem is shown on the news page''',
            },
        },
    }
