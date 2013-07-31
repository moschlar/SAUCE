# -*- coding: utf-8 -*-
'''
Created on May 14, 2013

@author: moschlar
'''

import tw2.core as twc
import tw2.bootstrap.forms as twb
import tw2.bootstrap.wysihtml5 as twbw


__all__ = [
    'Wysihtml5',
    'MediumTextField',
    'SmallTextField',
    'CalendarDateTimePicker',
]


class LargeMixin(object):
    css_class = 'span8'


class MediumMixin(object):
    css_class = 'span4'


class SmallMixin(object):
    css_class = 'span2'


class Wysihtml5(LargeMixin, twbw.Wysihtml5):
    rows = 3
    wysihtml5_args = {
        'html': True,
    }


class MediumTextField(MediumMixin, twb.TextField):
    pass


class SmallTextField(SmallMixin, twb.TextField):
    pass


class CalendarDateTimePicker(SmallMixin, twb.CalendarDateTimePicker):

    datetimepicker_args = {
        'weekStart': 1,
        'autoClose': True,
        'todayBtn': True,
        'todayHighlight': True,
        'minuteStep': 15,
    }

    @classmethod
    def post_define(cls):
        from tg import config
        try:
            # Use configured D_T_FMT without seconds
            cls.date_format = config.D_T_FMT.replace('%%', '%').replace(':%S', '')
        except AttributeError:
            pass


class VisibilitySelectField(twb.VerticalRadioButtonTable):

    options = [
        (u'anonymous', u'Anonymous (Everyone)'),
        (u'users', u'Users (Users that are logged in)'),
        (u'students', u'Students (Users enrolled in this event)'),
        (u'tutors', u'Tutors (Users that are tutors in this event)'),
        (u'teachers', u'Teachers (Users that are teachers in this event)'),
    ]
    cols = 2

    css_class = ""

    help_text = u'''Keep in mind that all superior objects must also allow access
    for these settings to be honored.'''
