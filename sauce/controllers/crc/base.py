# -*- coding: utf-8 -*-
'''Custom CrudContoller base class

@see: :mod:`tgext.crud`
@see: :mod:`sprox`

@since: 15.04.2012
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

from itertools import groupby
from webhelpers.html.builder import literal

from tg import expose, tmpl_context as c, request, flash, abort
from tg.decorators import before_validate, before_render, override_template, with_trailing_slash
from tg.controllers.tgcontroller import TGController
from tgext.crud import CrudRestController, EasyCrudRestController
from tgext.crud.controller import CrudRestControllerHelpers

from sauce.model import DBSession

import tw2.core as twc
import tw2.bootstrap.forms as twb
import tw2.jqplugins.chosen.widgets as twjc
import sprox.widgets.tw2widgets.widgets as sw
from sauce.widgets.datagrid import JSSortableDataGrid
from sauce.widgets.widgets import LargeMixin, SmallMixin, Wysihtml5, MediumTextField, SmallTextField, CalendarDateTimePicker

from sprox.sa.widgetselector import SAWidgetSelector
from sauce.controllers.crc.provider import FilterSAORMSelector
from sprox.fillerbase import TableFiller, AddFormFiller, EditFormFiller
from sprox.formbase import AddRecordForm, EditableForm

import sqlalchemy.types as sqlat
import transaction
from sqlalchemy.exc import IntegrityError, DatabaseError, ProgrammingError
errors = (IntegrityError, DatabaseError, ProgrammingError)

import logging
log = logging.getLogger(__name__)

__all__ = ['FilterCrudRestController']


#--------------------------------------------------------------------------------


class ChosenPropertyMultipleSelectField(LargeMixin, twjc.ChosenMultipleSelectField, sw.PropertyMultipleSelectField):

    def _validate(self, value, state=None):
        # Fix inspired by twf.MultipleSelectionField
        if value and not isinstance(value, (list, tuple)):
            value = [value]
        return super(ChosenPropertyMultipleSelectField, self)._validate(value, state)


class ChosenPropertySingleSelectField(SmallMixin, twjc.ChosenSingleSelectField, sw.PropertySingleSelectField):
    pass


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
        'description': Wysihtml5,
        'message': Wysihtml5,
    }

    def __init__(self, *args, **kwargs):
        self.default_widgets.update({
            sqlat.String:     MediumTextField,
            sqlat.Integer:    SmallTextField,
            sqlat.Numeric:    SmallTextField,
            sqlat.DateTime:   CalendarDateTimePicker,
            sqlat.Date:       twb.CalendarDatePicker,
            sqlat.Time:       twb.CalendarTimePicker,
            sqlat.Binary:     twb.FileField,
            sqlat.BLOB:       twb.FileField,
            sqlat.PickleType: MediumTextField,
            sqlat.Enum:       twjc.ChosenSingleSelectField,
        })
        super(MyWidgetSelector, self).__init__(*args, **kwargs)

    def select(self, field):
        widget = super(MyWidgetSelector, self).select(field)
        if issubclass(widget, sw.TextArea) \
                and hasattr(field.type, 'length') \
                and (field.type.length is None or field.type.length < self.text_field_limit):
            widget = MediumTextField
        return widget


#--------------------------------------------------------------------------------


class CrudIndexController(TGController):
    '''Controller for a crud index page

    Will show menu in the same way that CrudControllers do and nothing else.
    Therefore mocks some of the stuff from CrudRestController
    '''

    def __init__(self, *args, **kw):
        super(CrudIndexController, self).__init__(*args, **kw)
        self.helpers = CrudRestControllerHelpers()

    def _before(self, *args, **kw):
        '''Set values needed in tmpl_context'''
        c.title = self.title
        c.menu_items = self.menu_items
        #c.kept_params = self._kept_params()
        c.crud_helpers = self.helpers
        #c.crud_style = self.style

    @with_trailing_slash
    @expose('sauce.templates.crc.index')
    def index(self, *args, **kwargs):
        return dict(page='event')


#--------------------------------------------------------------------------------

class FilterCrudRestController(EasyCrudRestController):
    '''Generic base class for CrudRestControllers with filters'''

    mount_point = '.'
    substring_filters = True

    def __init__(self, query_modifier=None, query_modifiers=None,
                 menu_items=None, inject=None, hints=None,
                 allow_new=True, allow_edit=True, allow_delete=True,
                 **kwargs):
        '''Initialize FilteredCrudRestController with given options

        :param query_modifier: A callable that may modify the base query from the model entity
        :type query_modifier: callable | None
        :param query_modifiers:
            A dict of callable that may modify the relationship query from the model entity
            the keys are the remote side classes
        :type query_modifiers: dict
        :param menu_items: A dict of menu_items for ``EasyCrudRestController``
        :type menu_items: dict
        :param inject: A dict of values to inject into POST requests before validation
        :type inject: dict
        :param hints: Additional information that will be passed to the table_filler attribute
        :param allow_new:
            Whether the "New <Entity>" link shall be displayed on get_all
            and the url /<entity/new will be accessible
        :type allow_new: bool
        :param allow_edit:
            Whether the "Edit" link shall be displayed in the actions column
            on get_all and the url /<entity/<id>/delete will be accessible
        :type allow_edit: bool
        :param allow_delete:
            Whether the "Delete" link shall be displayed in the actions column
            on get_all and the url /<entity/<id>/delete will be accessible
        :type allow_delete: bool
        '''

        self.query_modifier = query_modifier
        self.query_modifiers = query_modifiers or {}

        self.inject = inject or {}
        self.hints = hints or {}

        self.allow_new = allow_new
        self.allow_edit = allow_edit
        self.allow_delete = allow_delete

#        if not hasattr(self, 'table'):
#            class Table(JSSortableTableBase):
#                __entity__ = self.model
#            self.table = Table(DBSession)

        # To effectively disable pagination and fix issues with tgext.crud.util.SmartPaginationCollection
        if not hasattr(self, 'table_filler'):
            class MyTableFiller(TableFiller):
                __model__ = __entity__ = self.model
                __actions__ = self.custom_actions
                __provider_type_selector_type__ = FilterSAORMSelector
                query_modifier = self.query_modifier
                query_modifiers = self.query_modifiers
                hints = self.hints
            self.table_filler = MyTableFiller(DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers,
                hints=self.hints)

        if self.allow_edit and not hasattr(self, 'edit_form'):
            class EditForm(EditableForm):
                __model__ = __entity__ = self.model
                __provider_type_selector_type__ = FilterSAORMSelector
                def _do_get_validator_args(self, field_name, field, validator_type):
                    args = super(EditForm, self)._do_get_validator_args(field_name, field, validator_type)
                    widget_type = self._do_get_field_wiget_type(field_name, field)
                    if widget_type and issubclass(widget_type, (twb.CalendarDatePicker, twb.CalendarDateTimePicker)):
                        widget_args = EditForm.__base__.__base__.__base__._do_get_field_widget_args(self, field_name, field)
                        args['format'] = widget_args.get('date_format', widget_type.date_format)
                    return args
            self.edit_form = EditForm(DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers)

        if self.allow_edit and not hasattr(self, 'edit_filler'):
            class EditFiller(EditFormFiller):
                __model__ = __entity__ = self.model
                __provider_type_selector_type__ = FilterSAORMSelector
            self.edit_filler = EditFiller(DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers)

        if self.allow_new and not hasattr(self, 'new_form'):
            class NewForm(AddRecordForm):
                __model__ = __entity__ = self.model
                __provider_type_selector_type__ = FilterSAORMSelector
                def _do_get_validator_args(self, field_name, field, validator_type):
                    args = super(NewForm, self)._do_get_validator_args(field_name, field, validator_type)
                    widget_type = self._do_get_field_wiget_type(field_name, field)
                    if widget_type and issubclass(widget_type, (twb.CalendarDatePicker, twb.CalendarDateTimePicker)):
                        widget_args = NewForm.__base__.__base__.__base__._do_get_field_widget_args(self, field_name, field)
                        args['format'] = widget_args.get('date_format', widget_type.date_format)
                    return args
            self.new_form = NewForm(DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers)

        if self.allow_new and not hasattr(self, 'new_filler'):
            class NewFiller(AddFormFiller):
                __model__ = __entity__ = self.model
                __provider_type_selector_type__ = FilterSAORMSelector
            self.new_filler = NewFiller(DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers)

        # Now this is some ugly hackery needed for the JSSortableDataGrid...
        self.__table_options__['__base_widget_type__'] = JSSortableDataGrid
        if '__base_widget_args__' in self.__table_options__:
            if 'headers' in self.__table_options__['__base_widget_args__']:
                self.__table_options__['__base_widget_args__']['headers'].update({0: {'sorter': False}})
            else:
                self.__table_options__['__base_widget_args__'].update({'headers': {0: {'sorter': False}}})
        else:
            self.__table_options__['__base_widget_args__'] = {'headers': {0: {'sorter': False}}}

        self.__form_options__['__base_widget_type__'] = twb.HorizontalForm
        self.__form_options__['__widget_selector__'] = MyWidgetSelector()

        if '__search_fields__' in self.__table_options__:
            self.search_fields = self.__table_options__['__search_fields__']

        # Since DBSession is a scopedsession we don't need to pass it around,
        # so we just use the imported DBSession here
        super(FilterCrudRestController, self).__init__(DBSession, menu_items)

    def custom_actions(self, obj):
        ''''Display bootstrap-styled action fields respecting the allow_* properties'''
        result = []
        count = 0
        try:
            result.append(u'<a href="' + obj.url + '" class="btn btn-mini" title="Show">'
                u'<i class="icon-eye-open"></i></a>')
            count += 1
        except:
            pass
        if self.allow_edit:
            try:
                primary_fields = self.table_filler.__provider__.get_primary_fields(self.table_filler.__entity__)
                pklist = u'/'.join(map(lambda x: unicode(getattr(obj, x)), primary_fields))
                result.append(u'<a href="' + pklist + '/edit" class="btn btn-mini" title="Edit">'
                    u'<i class="icon-pencil"></i></a>')
            except:
                pass
        if self.allow_delete:
            result.append(
                u'<a class="btn btn-mini btn-danger" href="./%d/delete" title="Delete">'
                u'  <i class="icon-remove icon-white"></i>'
                u'</a>' % (obj.id))
        return literal('<div class="btn-group" style="width: %dpx;">'
            % (len(result) * 30) + ''.join(result) + '</div>')

    def _before(self, *args, **kw):
        super(FilterCrudRestController, self)._before(*args, **kw)
        # Legacy compliance
        try:
            c.menu_item = self.menu_item
        except:
            c.menu_item = self.model.__name__

    @expose('sauce.templates.crc.get_delete')
    def get_delete(self, *args, **kw):
        '''This is the code that creates a confirm_delete page

        The delete operation will be simulated to be able to display all related
        objects that would be deleted too.
        '''
        if not self.allow_delete:
            abort(403)
        pks = self.provider.get_primary_fields(self.model)
        kw, d = {}, {}
        for i, pk in enumerate(pks):
            kw[pk] = args[i]
        for i, arg in enumerate(args):
            d[pks[i]] = arg

        obj = self.provider.delete(self.model, d)
        deps = u'<dl>'
        for k, g in groupby(sorted(o for o in DBSession.deleted if o != obj), lambda x: type(x)):
            deps += u'<dt>' + unicode(k.__name__) + u'</dt>'
            deps += u'<dd>' + u', '.join(sorted(unicode(o) for o in g)) + u'</dd>'
        deps += u'</dl>'

        transaction.doom()

        #obj = self.edit_filler.__provider__.get_obj(self.model, params=kw, fields=self.edit_filler.__fields__)
        pklist = u'/'.join(map(lambda x: unicode(getattr(obj, x)), pks))

        return dict(obj=obj,
            model=self.model.__name__,
            deps=deps,
            pk_count=len(pks), pklist=pklist)

    @staticmethod
    def before_get_all(remainder, params, output):
        '''Function to be hooked before get_all

        - Disables pagination
        - Replaces template with our own
        - Sets allow_* switches in tmpl_context
        '''
        # Disable pagination for get_all
        output['value_list'].page_count = 0
        #output['value_list'] = output['value_list'].original_collection
        output['value_list'] = output['value_list'].collection
        c.paginators = []

        # Use my bootstrap-enabled template
        override_template(FilterCrudRestController.get_all,
            'mako:sauce.templates.crc.get_all')

        self = request.controller_state.controller

        for allow in ('allow_new', 'allow_edit', 'allow_delete'):
            setattr(c, allow, getattr(self, allow, True))

    @staticmethod
    def before_new(remainder, params, output):
        '''Function to be hooked before new

        - Determines whether creating is even allowed
        - Replaces template with our own
        '''
        self = request.controller_state.controller
        if not getattr(self, 'allow_new', True):
            abort(403)
        # Use my bootstrap-enabled template
        override_template(FilterCrudRestController.new,
            'mako:sauce.templates.crc.new')

    @staticmethod
    def before_edit(remainder, params, output):
        '''Function to be hooked before edit

        - Determines whether editing is even allowed
        - Replaces template with our own
        '''
        self = request.controller_state.controller
        if not getattr(self, 'allow_edit', True):
            abort(403)
        # Use my bootstrap-enabled template
        override_template(FilterCrudRestController.edit,
            'mako:sauce.templates.crc.edit')

    @staticmethod
    def injector(remainder, params):
        '''Injects the modifiers from self.inject into params

        self.inject has to be a dictionary of key, object pairs
        '''
        # Get currently dispatched controller instance
        # Does not work, only returns last statically dispatch controller,
        # but we use _lookup in EventsController
        #s = dispatched_controller()
        self = request.controller_state.controller

        for k in getattr(self, 'inject', []):
            params[k] = self.inject[k]


# Register injection hook for POST requests
before_validate(FilterCrudRestController.injector)(FilterCrudRestController.post)

# Register hook for get_all
before_render(FilterCrudRestController.before_get_all)(FilterCrudRestController.get_all)
# Register hook for new
before_render(FilterCrudRestController.before_new)(FilterCrudRestController.new)
# Register hook for edit
before_render(FilterCrudRestController.before_edit)(FilterCrudRestController.edit)
