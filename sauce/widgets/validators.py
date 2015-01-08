# -*- coding: utf-8 -*-
'''Auxiliary validators for SAUCE widgets

@since: 2015-01-07
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

from tg.i18n import ugettext as _
import tw2.core as twc
from sqlalchemy.orm.exc import NoResultFound
from sauce.lib.sanitize import bleach
from functools import partial

try:
    _()
except TypeError:
    _ = lambda x: x


class FloatValidator(twc.validation.RangeValidator):
    """
    Confirm the value is an integer. This is derived from
    :class:`RangeValidator` so `min` and `max` can be specified.
    """
    msgs = {
        'notfloat': _('Must be a float'),
    }

    def to_python(self, value, state=None):
        value = super(FloatValidator, self).to_python(value, state)
        try:
            if value is None or unicode(value) == '':
                return None
            else:
                return float(value)
        except ValueError:
            raise twc.validation.ValidationError('notfloat', self)

    def _validate_python(self, value, state=None):
        if self.required and value is None:
            raise twc.validation.ValidationError('required', self)
        if value is not None:
            if self.min and value < self.min:
                raise twc.validation.ValidationError('toosmall', self)
            if self.max and value > self.max:
                raise twc.validation.ValidationError('toobig', self)

    def from_python(self, value, state=None):
        if value is None:
            return None
        else:
            return unicode(value)


class UniqueValidator(twc.Validator):

    msgs = {
        'notunique': _('Not unique'),
    }

    def __init__(self, entity, key, allowed_values=None, **kw):
        super(UniqueValidator, self).__init__(**kw)
        self.entity = entity
        self.key = key
        self.allowed_values = allowed_values or []

    def _validate_python(self, value, state=None):
        if value in self.allowed_values:
            return value
        try:
            self.entity.query.filter_by(**{self.key: value}).one()
        except NoResultFound:
            return value
        else:
            raise twc.ValidationError('notunique', self)


class BleachValidator(twc.StringLengthValidator):
    ruleset = None
    clean_func = None
    bleach_kwargs = None

    def __init__(self, ruleset=None, clean_func=None, bleach_kwargs=None, **kw):
        if ruleset:
            self.ruleset = ruleset
        if clean_func:
            self.clean_func = clean_func
        else:
            self.clean_func = partial(bleach, ruleset=self.ruleset)
        self.bleach_kwargs = bleach_kwargs or {}
        super(BleachValidator, self).__init__(**kw)

    def _convert_to_python(self, value, state=None):
        value = self.clean_func(value, **self.bleach_kwargs)
        return value


class BasicWysihtml5BleachValidator(BleachValidator):
    ruleset = 'basic'


class SimpleWysihtml5BleachValidator(BleachValidator):
    ruleset = 'simple'


class AdvancedWysihtml5BleachValidator(BleachValidator):
    ruleset = 'advanced'
