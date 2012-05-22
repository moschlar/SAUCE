# -*- coding: utf-8 -*-
"""Sheets controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, abort, tmpl_context as c, flash, TGController
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
from repoze.what.predicates import has_permission, Any
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.auth import has_teacher, is_public
from sauce.model import Sheet
from sauce.controllers.assignments import AssignmentsController
from sauce.lib.menu import entity_menu

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
    
    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.side_menu = entity_menu(self.sheet, 'Assignments', self.sheet.assignments)
    
    @expose('sauce.templates.sheet')
    def index(self):
        '''Sheet details page'''
        
        return dict(page='sheets', event=self.event, sheet=self.sheet)
    

class SheetsController(TGController):
    
    def __init__(self, event):
        
        self.event = event
    
    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.side_menu = entity_menu(self.event, 'Sheets', self.event.sheets)
    
    @expose('sauce.templates.sheets')
    def index(self, page=1):
        '''Sheet listing page'''
        
        sheets = Page(self.event.current_sheets, page=page, items_per_page=10)
        previous_sheets = Page(self.event.previous_sheets, page=page, items_per_page=10)
        future_sheets = Page(self.event.future_sheets, page=page, items_per_page=10)
        
        return dict(page='sheets', event=self.event, sheets=sheets,
                    previous_sheets=previous_sheets, future_sheets=future_sheets)
    
    @expose()
    def _lookup(self, sheet_id, *args):
        '''Return SheetController for specified sheet_id'''
        
        try:
            sheet_id = int(sheet_id)
            sheet = Sheet.by_sheet_id(sheet_id, self.event)
        except ValueError:
            flash('Invalid Sheet id: %s' % sheet_id,'error')
            abort(400)
        except NoResultFound:
            flash('Sheet %d not found' % sheet_id,'error')
            abort(404)
        except MultipleResultsFound:
            log.error('Database inconsistency: Sheet %s' % sheet_id, exc_info=True)
            flash('An error occurred while accessing Sheet %d' % sheet_id,'error')
            abort(500)
        
        controller = SheetController(sheet)
        return controller, args
