# -*- coding: utf-8 -*-
'''Collection of miscellaneous widgets for SAUCE

@see: :mod:`tw2.core`

@since: May 14, 2013
@author: moschlar
'''

import tw2.core as twc
import tw2.bootstrap.forms as twb
import tw2.bootstrap.wysihtml5 as twbw

import tw2.ace as twa

from tg import config


__all__ = [
    'Wysihtml5',
    'MediumTextField',
    'SmallTextField',
    'LargeTextArea',
    'CalendarDateTimePicker',
]


class LargeMixin(object):
    css_class = 'span8'


class MediumMixin(object):
    css_class = 'span4'


class SmallMixin(object):
    css_class = 'span2'


class Wysihtml5(LargeMixin, twbw.Wysihtml5):
    cols = 80
    rows = 8
    parser = False
    wysihtml5_args = {
        'html': True,
    }


class SourceEditor(LargeMixin, twa.AceWidget):
    cols = 80
    rows = 8
    soft_wrap = False


class MediumTextField(MediumMixin, twb.TextField):
    pass


class SmallTextField(SmallMixin, twb.TextField):
    pass


class LargeTextArea(LargeMixin, twb.TextArea):
    pass


class CalendarDateTimePicker(SmallMixin, twb.CalendarDateTimePicker):

    datetimepicker_args = {
        'weekStart': 1,
        'autoClose': True,
        'todayBtn': True,
        'todayHighlight': True,
        'minuteStep': 15,
    }
    date_format = config.D_T_FMT
