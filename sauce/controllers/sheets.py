# -*- coding: utf-8 -*-
"""Sheet controller module"""

import logging

# turbogears imports
from tg import expose, url, flash, redirect, request, abort, tmpl_context as c
#from tg import redirect, validate, flash

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _

from tg.decorators import require
from repoze.what.predicates import not_anonymous

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, Sheet, Submission, Language, Student, Event
from sauce.widgets.submit import submit_form
import transaction

log = logging.getLogger(__name__)

class SheetController(object):
    
    def __init__(self, sheet_id):
        
        self.sheet_id = sheet_id
        
        try:
            self.sheet = DBSession.query(Sheet).filter(Sheet.id == self.sheet_id).one()
        except NoResultFound:
            abort(404, 'Sheet %d not found' % self.sheet_id, 
                  comment='Sheet %d not found' % self.sheet_id)
        
        self.event = self.sheet.event
        
    @expose('sauce.templates.sheet')
    def index(self):
        
        return dict(page='sheets', event=self.event, sheet=self.sheet)

class SheetsController(BaseController):
    
    def __init__(self, event_id=None):
        if event_id:
            self.event_id = event_id
            self.event = DBSession.query(Event).filter_by(id=self.event_id).one()
        else:
            self.event_id = None
            self.event = None
        
    @expose('sauce.templates.sheets')
    def index(self):
        
        #sheets = Page(Sheet.current_sheets(event=self.event, only_public=False), page=page, items_per_page=10)
        all_sheets = Sheet.all_sheets(self.event, only_public=False)
        
        return dict(page='sheets', event=self.event, all_sheets=all_sheets)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return SheetController for specified id'''
        
        sheet_id = int(id)
        controller = SheetController(sheet_id)
        return controller, args
