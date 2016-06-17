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

import status

from tg import expose, tmpl_context as c, request, abort
from tg.decorators import before_validate, before_render, override_template, with_trailing_slash
from tg.controllers.tgcontroller import TGController
from tgext.crud import EasyCrudRestController
from tgext.crud.controller import CrudRestControllerHelpers

from sauce.model import DBSession

import tw2.bootstrap.forms as twb
from sauce.widgets.datagrid import JSSortableDataGrid
from sauce.controllers.crc.provider import FilterSAORMSelector
from sauce.controllers.crc.formbase import MyAddForm, MyEditForm
from sauce.controllers.crc.fillerbase import MyTableFiller, MyAddFormFiller, MyEditFormFiller

import transaction
from sqlalchemy.exc import IntegrityError, DatabaseError, ProgrammingError
errors = (IntegrityError, DatabaseError, ProgrammingError)

import logging
log = logging.getLogger(__name__)

__all__ = ['FilterCrudRestController']


#--------------------------------------------------------------------------------

# Monkeypatching yeah
import tgext.crud.controller
tgext.crud.controller.ProviderTypeSelector = FilterSAORMSelector

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
    resources = ()

    def __init__(self, query_modifier=None, query_modifiers=None,
                 menu_items=None, inject=None, hints=None,
                 allow_new=True, allow_edit=True, allow_delete=True, allow_copy=False,
                 show_menu=True,
                 **kwargs):  # pylint:disable=too-many-arguments
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
        :param show_menu:
            Whether the menu sidebar shall be shown or hidden
        :type show_menu: bool
        '''

        self.query_modifier = query_modifier
        self.query_modifiers = query_modifiers or {}

        self.inject = inject or {}
        self.hints = hints or {}

        self.allow_new = allow_new
        self.allow_edit = allow_edit
        self.allow_delete = allow_delete
        self.allow_copy = allow_copy

        self.show_menu = show_menu

#        if not hasattr(self, 'table'):
#            class Table(JSSortableTableBase):
#                __entity__ = self.model
#            self.table = Table(DBSession)

        # To effectively disable pagination and fix issues with tgext.crud.util.SmartPaginationCollection
        self.table_filler = MyTableFiller(self.model, self.actions, DBSession,
            query_modifier=self.query_modifier, query_modifiers=self.query_modifiers,
            hints=self.hints)

        if self.allow_edit:
            self.edit_form = MyEditForm(self.model, DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers,
                hints=self.hints)
            self.edit_filler = MyEditFormFiller(self.model, DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers,
                hints=self.hints)
        else:
            self.edit_form = None
            self.edit_filler = None

        if self.allow_new:
            self.new_form = MyAddForm(self.model, DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers,
                hints=self.hints)
            self.new_filler = MyAddFormFiller(self.model, DBSession,
                query_modifier=self.query_modifier, query_modifiers=self.query_modifiers,
                hints=self.hints)
        else:
            self.new_form = None
            self.new_filler = None

        # Now this is some ugly hackery needed for the JSSortableDataGrid...
        self.__table_options__['__base_widget_type__'] = JSSortableDataGrid
        if '__base_widget_args__' in self.__table_options__:
            if 'headers' in self.__table_options__['__base_widget_args__']:
                self.__table_options__['__base_widget_args__']['headers'].update({0: {'sorter': False}})
            else:
                self.__table_options__['__base_widget_args__'].update({'headers': {0: {'sorter': False}}})
        else:
            self.__table_options__['__base_widget_args__'] = {'headers': {0: {'sorter': False}}}

        if '__search_fields__' in self.__table_options__:
            self.search_fields = self.__table_options__['__search_fields__']

        self.__form_options__['__base_widget_type__'] = twb.HorizontalForm

        # Since DBSession is a scopedsession we don't need to pass it around,
        # so we just use the imported DBSession here
        super(FilterCrudRestController, self).__init__(DBSession, menu_items)

        # tgext.crud is a little bit harsh about the ProviderTypeSelector...
        self.provider = FilterSAORMSelector().get_selector(self.model).get_provider(entity=self.model, hint=DBSession,
            query_modifier=self.query_modifier, query_modifiers=self.query_modifiers)

    def _actions(self, obj):
        ''''Make list of action links respecting the allow_* properties'''
        actions = []
        try:
            actions.append(u'<a href="' + obj.url + '" class="btn btn-mini" title="Show">'
                u'<i class="icon-eye-open"></i></a>')
        except:
            pass
        if self.allow_edit:
            try:
                primary_fields = self.table_filler.__provider__.get_primary_fields(self.table_filler.__entity__)
                pklist = u'/'.join(map(lambda x: unicode(getattr(obj, x)), primary_fields))
                actions.append(u'<a href="' + pklist + '/edit" class="btn btn-mini" title="Edit">'
                    u'<i class="icon-pencil"></i></a>')
            except:
                pass
        if self.allow_delete:
            actions.append(
                u'<a class="btn btn-mini btn-danger" href="./%d/delete" title="Delete">'
                u'  <i class="icon-remove icon-white"></i>'
                u'</a>' % (obj.id))
        return actions

    def actions(self, obj):
        ''''Display bootstrap-styled action links respecting the allow_* properties'''
        actions = self._actions(obj)
        if actions:
            return literal(u'<div class="btn-group" style="width: %dpx;">'
                % (len(actions) * 30) + ''.join(actions) + u'</div>')
        else:
            return u''

    def _bulk_actions(self):
        bulk_actions = []
        if self.allow_new:
            bulk_actions.append(u'<a href="./new" class="btn"><i class="icon-plus-sign"></i>&nbsp;New %s</a>' % (self.model.__name__))
        if self.allow_copy:
            bulk_actions.append(u'<a href="./copy" class="btn"><i class="icon-share-alt"></i>&nbsp;Copy %s</a>' % (self.model.__name__))
        return bulk_actions

    def bulk_actions(self):
        ''''Display bootstrap-styled action links respecting the allow_* properties'''
        bulk_actions = self._bulk_actions()
        if bulk_actions:
            return literal(u'<div class="btn-group">' + ''.join(bulk_actions) + '</div>')
        else:
            return u''

    def _before(self, *args, **kw):
        super(FilterCrudRestController, self)._before(*args, **kw)
        # Legacy compliance
        try:
            c.menu_item = self.menu_item
        except:
            c.menu_item = self.model.__name__
        for show in ('show_menu', ):
            setattr(c, show, getattr(self, show, True))

    @expose('sauce.templates.crc.get_delete')
    def get_delete(self, *args, **kw):
        '''This is the code that creates a confirm_delete page

        The delete operation will be simulated to be able to display all related
        objects that would be deleted too.
        '''
        if not self.allow_delete:
            abort(status.HTTP_403_FORBIDDEN)
        pks = self.provider.get_primary_fields(self.model)
        kw, d = {}, {}
        for i, pk in enumerate(pks):
            kw[pk] = args[i]
        for i, arg in enumerate(args):
            d[pks[i]] = arg

        obj = self.provider.delete(self.model, d)
        deps = u'<dl>'
        for k, g in groupby(sorted(o for o in DBSession.deleted if o != obj), lambda x: type(x)):
            deps += u'<dt>' + unicode(k.__name__) + u's' + u'</dt>'
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
    def before_render_get_all(remainder, params, output):
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

        try:
            c.bulk_actions = self.bulk_actions()
        except:  # tgext.admin
            c.bulk_actions = u'<a href="./new" class="btn"><i class="icon-plus-sign"></i>&nbsp;New %s</a>' % self.model.__name__

        for allow in ('allow_new', 'allow_edit', 'allow_delete'):
            setattr(c, allow, getattr(self, allow, True))

    @staticmethod
    def before_render_new(remainder, params, output):
        '''Function to be hooked before new

        - Determines whether creating is even allowed
        - Replaces template with our own
        '''
        self = request.controller_state.controller
        if not getattr(self, 'allow_new', True):
            abort(status.HTTP_403_FORBIDDEN)
        # Use my bootstrap-enabled template
        override_template(FilterCrudRestController.new,
            'mako:sauce.templates.crc.new')

    @staticmethod
    def before_render_edit(remainder, params, output):
        '''Function to be hooked before edit

        - Determines whether editing is even allowed
        - Replaces template with our own
        '''
        self = request.controller_state.controller
        if not getattr(self, 'allow_edit', True):
            abort(status.HTTP_403_FORBIDDEN)
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

        for k in getattr(self, 'inject', dict()):
            log.info('Injecting %r = %r into params %r for %r', k, self.inject[k], params, self.model)
            params[k] = self.inject[k]


# Register injection hook for POST requests
before_validate(FilterCrudRestController.injector)(FilterCrudRestController.post)

# Register hook for get_all
before_render(FilterCrudRestController.before_render_get_all)(FilterCrudRestController.get_all)
# Register hook for new
before_render(FilterCrudRestController.before_render_new)(FilterCrudRestController.new)
# Register hook for edit
before_render(FilterCrudRestController.before_render_edit)(FilterCrudRestController.edit)
