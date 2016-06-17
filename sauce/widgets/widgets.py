# -*- coding: utf-8 -*-
'''Collection of miscellaneous widgets for SAUCE

@see: :mod:`tw2.core`

@since: May 14, 2013
@author: moschlar
'''

import tw2.core as twc
import tw2.bootstrap.forms as twb
import tw2.bootstrap.wysihtml5 as twbw
from tw2.codemirror import CodeMirrorDisplay as _SourceDisplay, CodeMirrorEditor as _SourceEditor

from sauce.widgets.validators import AdvancedWysihtml5BleachValidator, SimpleWysihtml5BleachValidator

from tg import config


__all__ = [
    'MyHorizontalLayout',
    'AdvancedWysihtml5',
    'SimpleWysihtml5',
    'SourceDisplay',
    'LargeSourceEditor',
    'MediumSourceEditor',
    'SmallSourceEditor',
    'MediumTextField',
    'SmallTextField',
    'LargeTextArea',
    'CalendarDateTimePicker',
]


class MyHorizontalLayout(twb.HorizontalLayout):

    @property
    def children_non_hidden(self):
        return [c for c in super(MyHorizontalLayout, self).children_non_hidden
            if not getattr(c, 'no_display', None)]



class LargeMixin(object):
    css_class = 'span8'


class MediumMixin(object):
    css_class = 'span4'


class SmallMixin(object):
    css_class = 'span2'


class AdvancedWysihtml5(twbw.Wysihtml5):
    cols = 80
    rows = 8
    css_class = 'span8 wysihtml5ify'
#    stylesheets = ['/css/bootstrap.css']  # TODO
    validator = AdvancedWysihtml5BleachValidator
    parser = 'advanced'
    wysihtml5_args = {
        'html': True,
    }


class SimpleWysihtml5(twbw.Wysihtml5):
    cols = 80
    rows = 8
    css_class = 'span8 wysihtml5ify'
    validator = SimpleWysihtml5BleachValidator
    parser = 'simple'
    wysihtml5_args = {
        'font-styles': False,
        'image': False,
    }


class SourceDisplay(_SourceDisplay):
    selector = twc.Variable("Escaped id.  jQuery selector.")
    no_display = twc.Param('Whether the widget should not be rendered at all.', default=False)

    def prepare(self):
        if not self.value:
            self.no_display = True
        super(SourceDisplay, self).prepare()
        if 'id' in self.attrs:
            self.selector = "#" + self.attrs['id'].replace(':', '\\:')


class SourceEditor(_SourceEditor):
    disabled = True  # Make underlying textarea disabled for graceful degradation
    selector = twc.Variable("Escaped id.  jQuery selector.")

    def prepare(self):
        super(SourceEditor, self).prepare()
        if 'id' in self.attrs:
            self.selector = "#" + self.attrs['id'].replace(':', '\\:')


class LargeSourceEditor(LargeMixin, SourceEditor):
    cols = 80
    rows = 24


class MediumSourceEditor(LargeMixin, SourceEditor):
    cols = 80
    rows = 12


class SmallSourceEditor(LargeMixin, SourceEditor):
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

    def __init__(self, *args, **kwargs):
        self.date_format = config.D_T_FMT
        super(CalendarDateTimePicker, self).__init__(*args, **kwargs)
