'''
Created on 25.05.2012

@author: moschlar
'''

from tg.i18n import ugettext as _, lazy_ugettext as l_
import tw2.core as twc
import tw2.forms as twf

class FloatValidator(twc.validation.RangeValidator):
    """
    Confirm the value is an integer. This is derived from
    :class:`RangeValidator` so `min` and `max` can be specified.
    """
    msgs = {
        'notfloat': _('Must be a float'),
    }

    def to_python(self, value):
        value = super(FloatValidator, self).to_python(value)
        try:
            if value is None or str(value) == '':
                return None
            else:
                return float(value)
        except ValueError:
            raise twc.validation.ValidationError('notfloat', self)

    def validate_python(self, value, state=None):
        if self.required and value is None:
            raise twc.validation.ValidationError('required', self)
        if value is not None:
            if self.min and value < self.min:
                raise twc.validation.ValidationError('toosmall', self)
            if self.max and value > self.max:
                raise twc.validation.ValidationError('toobig', self)

    def from_python(self, value):
        if value is None:
            return None
        else:
            return str(value)

