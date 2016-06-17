'''

@since: 2015-01-03
@author: moschlar
'''

import tw2.bootstrap.forms as twb

from sprox.viewbase import ViewBase
from sprox.formbase import AddRecordForm, EditableForm

from sauce.controllers.crc.provider import FilterSAORMSelector


class MyEditForm(EditableForm):

    __provider_type_selector_type__ = FilterSAORMSelector
    __base_widget_type__ = twb.HorizontalForm

    def __init__(self, model, session, query_modifier=None, query_modifiers=None, hints=None):  # pylint:disable=too-many-arguments
        self.__model__ = self.__entity__ = model
        super(MyEditForm, self).__init__(session,
            query_modifier=query_modifier, query_modifiers=query_modifiers, hints=hints)

    def _do_get_validator_args(self, field_name, field, validator_type):  # @IgnorePep8
        args = super(MyEditForm, self)._do_get_validator_args(field_name, field, validator_type)
        widget_type = self._do_get_field_wiget_type(field_name, field)
        if widget_type and issubclass(widget_type, (twb.CalendarDatePicker, twb.CalendarDateTimePicker)):
            assert isinstance(self, ViewBase)
            widget_args = ViewBase._do_get_field_widget_args(self, field_name, field)
            args['format'] = widget_args.get('date_format', widget_type.date_format)
        return args


class MyAddForm(AddRecordForm):

    __provider_type_selector_type__ = FilterSAORMSelector
    __base_widget_type__ = twb.HorizontalForm

    def __init__(self, model, session, query_modifier=None, query_modifiers=None, hints=None):  # pylint:disable=too-many-arguments
        self.__model__ = self.__entity__ = model
        super(MyAddForm, self).__init__(session,
            query_modifier=query_modifier, query_modifiers=query_modifiers, hints=hints)

    def _do_get_validator_args(self, field_name, field, validator_type):  # @IgnorePep8
        args = super(MyAddForm, self)._do_get_validator_args(field_name, field, validator_type)
        widget_type = self._do_get_field_wiget_type(field_name, field)
        if widget_type and issubclass(widget_type, (twb.CalendarDatePicker, twb.CalendarDateTimePicker)):
            assert isinstance(self, ViewBase)
            widget_args = ViewBase._do_get_field_widget_args(self, field_name, field)
            args['format'] = widget_args.get('date_format', widget_type.date_format)
        return args
