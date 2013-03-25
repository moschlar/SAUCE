# -*- coding: utf-8 -*-
"""Sheets controller module

@author: moschlar
"""
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

import logging

# turbogears imports
from tg import expose, abort, tmpl_context as c, flash, TGController
from tg.decorators import paginate

# third party imports
#from tg.i18n import ugettext as _
from repoze.what.predicates import has_permission, Any
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.auth import has_teacher, is_public
from sauce.model import Sheet
from sauce.controllers.assignments import AssignmentsController
from sauce.lib.menu import menu
from sauce.controllers.lessons import SubmissionsController

log = logging.getLogger(__name__)


class SheetController(TGController):

    def __init__(self, sheet):
        self.sheet = sheet
        self.event = sheet.event
        self.assignments = AssignmentsController(sheet=self.sheet)
        c.sheet = self.sheet

        self.allow_only = Any(is_public(self.sheet),
                              has_teacher(self.sheet),
                              has_teacher(self.event),
                              has_permission('manage'),
                              msg=u'This Sheet is not public'
                              )

        self.submissions = SubmissionsController(sheet=self.sheet)

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.sheet)

    @expose('sauce.templates.sheet')
    def index(self):
        '''Sheet details page'''
        return dict(page='sheets', event=self.event, sheet=self.sheet)


class SheetsController(TGController):

    def __init__(self, event):
        self.event = event

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.event)

    @expose('sauce.templates.sheets')
    @paginate('current_sheets', use_prefix=True)
    @paginate('previous_sheets', use_prefix=True)
    @paginate('future_sheets', use_prefix=True)
    def index(self):
        '''Sheet listing page'''
        current_sheets = self.event.current_sheets
        previous_sheets = self.event.previous_sheets
        future_sheets = self.event.future_sheets

        return dict(page='sheets', event=self.event, current_sheets=current_sheets,
                    previous_sheets=previous_sheets, future_sheets=future_sheets)

    @expose()
    def _lookup(self, sheet_id, *args):
        '''Return SheetController for specified sheet_id'''
        try:
            sheet_id = int(sheet_id)
            sheet = Sheet.by_sheet_id(sheet_id, self.event)
        except ValueError:
            flash('Invalid Sheet id: %s' % sheet_id, 'error')
            abort(400)
        except NoResultFound:
            flash('Sheet %d not found' % sheet_id, 'error')
            abort(404)
        except MultipleResultsFound:
            log.error('Database inconsistency: Sheet %s' % sheet_id, exc_info=True)
            flash('An error occurred while accessing Sheet %d' % sheet_id, 'error')
            abort(500)

        controller = SheetController(sheet)
        return controller, args
