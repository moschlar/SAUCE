# -*- coding: utf-8 -*-
'''
Created on 15.04.2012

@author: moschlar
'''

from tg import expose, tmpl_context as c
from tg.decorators import paginate, with_trailing_slash
from tgext.crud import CrudRestController, EasyCrudRestController
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller, FillerBase, EditFormFiller

from sauce.model import DBSession, Event, Lesson, Team, User
from sprox.formbase import AddRecordForm, EditableForm

#--------------------------------------------------------------------------------

class FilteredCrudRestController(EasyCrudRestController):
    
    __table_options__ = {
        '__omit_fields__':[],
        '__field_order__':[],
        }
    __form_options__ = {
        '__hide_fields__':[],
        '__field_order__':[],
        '__field_widget_types__':{},
        }
    
    def __init__(self, session, model=None, filters=[], filter_bys=dict()):
        
        self.model = model
        super(FilteredCrudRestController, self).__init__(session)
        
        # Custom getter function respecting provided filters
        def custom_do_get_provider_count_and_objs(**kw):
            qry = model.query
            qry = qry.filter(*filters)
            qry = qry.filter_by(**filter_bys)
            objs = qry.all()
            return len(objs), objs
        
        self.table_filler._do_get_provider_count_and_objs = custom_do_get_provider_count_and_objs

#--------------------------------------------------------------------------------
