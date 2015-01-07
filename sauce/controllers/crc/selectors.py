'''

@since: 2015-01-07
@author: moschlar
'''

import sqlalchemy.types as sqlat

import tw2.core as twc
import tw2.bootstrap.forms as twb
import tw2.jqplugins.chosen.widgets as twjc
import sprox.widgets.tw2widgets.widgets as sw
from sprox.sa.widgetselector import SAWidgetSelector
from sprox.sa.validatorselector import SAValidatorSelector, Email
from sauce.widgets.widgets import (LargeMixin, SmallMixin, AdvancedWysihtml5,
    MediumTextField, SmallTextField, CalendarDateTimePicker)
from sauce.widgets.validators import AdvancedWysihtml5BleachValidator


class ChosenPropertyMultipleSelectField(LargeMixin, twjc.ChosenMultipleSelectField, sw.PropertyMultipleSelectField):

    search_contains = True

    def _validate(self, value, state=None):
        value = super(ChosenPropertyMultipleSelectField, self)._validate(value, state)
        if self.required and not value:
            raise twc.ValidationError('Please select at least one value')
        else:
            return value


class ChosenPropertySingleSelectField(SmallMixin, twjc.ChosenSingleSelectField, sw.PropertySingleSelectField):

    search_contains = True


class MyWidgetSelector(SAWidgetSelector):
    '''Custom WidgetSelector for SAUCE

    Primarily uses fields from tw2.bootstrap.forms and tw2.jqplugins.chosen.
    '''
    text_field_limit = 256
    default_multiple_select_field_widget_type = ChosenPropertyMultipleSelectField
    default_single_select_field_widget_type = ChosenPropertySingleSelectField

    default_name_based_widgets = {
        'name': MediumTextField,
        'subject': MediumTextField,
        '_url': MediumTextField,
        'user_name': MediumTextField,
        'email_address': MediumTextField,
        '_display_name': MediumTextField,
        'description': AdvancedWysihtml5,
        'message': AdvancedWysihtml5,
    }

    def __init__(self, *args, **kwargs):
        self.default_widgets.update({
            sqlat.String: MediumTextField,
            sqlat.Integer: SmallTextField,
            sqlat.Numeric: SmallTextField,
            sqlat.DateTime: CalendarDateTimePicker,
            sqlat.Date: twb.CalendarDatePicker,
            sqlat.Time: twb.CalendarTimePicker,
            sqlat.Binary: twb.FileField,
            sqlat.BLOB: twb.FileField,
            sqlat.PickleType: MediumTextField,
            sqlat.Enum: twjc.ChosenSingleSelectField,
        })
        super(MyWidgetSelector, self).__init__(*args, **kwargs)

    def select(self, field):
        widget = super(MyWidgetSelector, self).select(field)
        if (issubclass(widget, sw.TextArea)
                and hasattr(field.type, 'length')
                and (field.type.length is None or field.type.length < self.text_field_limit)):
            widget = MediumTextField
        return widget


class MyValidatorSelector(SAValidatorSelector):

    _name_based_validators = {
        'email_address': Email,
        'description': AdvancedWysihtml5BleachValidator,
        'message': AdvancedWysihtml5BleachValidator,
    }

    # def select(self, field):
    #     print 'MyValidatorSelector', 'select', field
    #     return super(MyValidatorSelector, self).select(field)
