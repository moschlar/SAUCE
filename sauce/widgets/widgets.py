# -*- coding: utf-8 -*-
'''Collection of miscellaneous widgets for SAUCE

@see: :mod:`tw2.core`

@since: May 14, 2013
@author: moschlar
'''

import tw2.core as twc
import tw2.bootstrap.forms as twb
import tw2.bootstrap.wysihtml5 as twbw

try:
#    from tw2.ace import AceWidget as _SourceEditor
    from tw2.codemirror import CodeMirrorWidget as _SourceEditor
except ImportError:  # pragma: no cover
    from tw2.bootstrap.forms import TextArea as _SourceEditor

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


class LargeSourceEditor(LargeMixin, _SourceEditor):
    cols = 80
    rows = 24


class MediumSourceEditor(LargeMixin, _SourceEditor):
    cols = 80
    rows = 12


class SmallSourceEditor(LargeMixin, _SourceEditor):
    cols = 80
    rows = 6


class MediumTextField(MediumMixin, twb.TextField):
    pass


class SmallTextField(SmallMixin, twb.TextField):
    pass


class LargeTextArea(LargeMixin, twb.TextArea):
    cols = 80


class CalendarDateTimePicker(SmallMixin, twb.CalendarDateTimePicker):

    datetimepicker_args = {
        'weekStart': 1,
        'autoClose': True,
        'todayBtn': True,
        'todayHighlight': True,
        'minuteStep': 15,
    }
    date_format = config.D_T_FMT
