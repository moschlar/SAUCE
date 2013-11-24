# -*- coding: utf-8 -*-
'''Auxiliary stuff for SAUCE widgets

Especially validators.

@since: 25.05.2012
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

    def __init__(self, entity, key, allowed_values=None):
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
