# -*- coding: utf-8 -*-
"""Sheet controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, abort, tmpl_context as c, url, validate, flash, redirect, request

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import Sheet, DBSession
from sauce.controllers.assignments import AssignmentsController

from sauce.widgets.sproxed import new_sheet_form, edit_sheet_form

log = logging.getLogger(__name__)

class SheetController(object):
    
    def __init__(self, sheet):
        
        self.sheet = sheet
        self.event = self.sheet.event
        
        self.assignments = AssignmentsController(sheet=self.sheet)
    
    @expose('sauce.templates.sheet')
    def index(self):
        '''Sheet details page'''
        
        return dict(page='sheets', breadcrumbs=self.sheet.breadcrumbs, event=self.event, sheet=self.sheet)
    
    @expose('sauce.templates.form')
    def edit(self, **kw):
        c.form = edit_sheet_form
        return dict(page='sheet', options=kw or self.sheet, child_args=dict(), action=url(self.sheet.url + '/post'))
    
    @expose()
    @validate(edit_sheet_form, error_handler=edit)
    def post(self, **kw):
        log.debug(kw)
        try:
            del kw['sprox_id']
            for key in kw:
                setattr(self.sheet, key, kw[key])
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            log.warning('Error modifying sheet', exc_info=True)
            flash('Error modifying sheet: %s' % e.message, 'error')
            redirect(url(self.sheet.url + '/edit'))
        else:
            flash('Sheet modified', 'ok')
            redirect(url(self.sheet.url))
        
        
class SheetsController(BaseController):
    
    def __init__(self, event):
        
        self.event = event
    
    @expose('sauce.templates.sheets')
    def index(self, page=1):
        '''Sheet listing page'''
        
        #sheets = Page(Sheet.current_sheets(event=self.event, only_public=False), page=page, items_per_page=10)
        sheets = Page(self.event.current_sheets, page=page, items_per_page=10)
        previous_sheets = Page(self.event.previous_sheets, page=page, items_per_page=10)
        future_sheets = Page(self.event.future_sheets, page=page, items_per_page=10)
        
        return dict(page='sheets', breadcrumbs=self.event.breadcrumbs, event=self.event, sheets=sheets, previous_sheets=previous_sheets, future_sheets=future_sheets)
    
    @expose('sauce.templates.form')
    def new(self, **kw):
        c.form = new_sheet_form
        if not hasattr(kw, 'teacher'):
            kw['teacher'] = request.teacher
        return dict(page='sheet', options=kw, child_args=dict(), action=url(self.event.url + '/sheets/post'))
    
    @expose()
    @validate(new_sheet_form, error_handler=new)
    def post(self, **kw):
        log.debug(kw)
        try:
            del kw['sprox_id']
            sheet = Sheet(event=self.event, **kw)
            DBSession.add(sheet)
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            log.warning('Error creating sheet', exc_info=True)
            flash('Error creating sheet: %s' % e.message, 'error')
            redirect(url(self.event.url + '/sheets'))
        else:
            flash('Sheet created', 'ok')
            redirect(url(sheet.url))
    
    @expose()
    def _lookup(self, sheet_id, *args):
        '''Return SheetController for specified sheet_id'''
        
        try:
            sheet_id = int(sheet_id)
            sheet = Sheet.by_sheet_id(sheet_id, self.event)
        except ValueError:
            abort(400)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        controller = SheetController(sheet)
        return controller, args
