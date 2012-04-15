# -*- coding: utf-8 -*-
"""Test controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, url, redirect, validate, flash, request, tmpl_context as c
from tg.decorators import paginate, with_trailing_slash
from tg.controllers import RestController
from tgext.crud import EasyCrudRestController, CrudRestController
# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Test, Assignment
from sauce.widgets.sproxed import new_test_form, test_table, test_table_filler, edit_test_form

log = logging.getLogger(__name__)

class TestController(EasyCrudRestController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    model = Test
    
    table = test_table
    table_filler = test_table_filler
    new_form = new_test_form
    edit_form = edit_test_form
    
    def __init__(self, assignment, *args, **kw):
        super(TestController, self).__init__(*args, **kw)
        self.assignment = assignment
    
    @with_trailing_slash
    @expose('tgext.crud.templates.get_all')
    @expose('json')
    @paginate('value_list', items_per_page=7)
    def get_all(self, *args, **kw):
        c.widget = self.table
        values = self.table_filler.get_value(assignment=self.assignment,**kw)
        return dict(model=self.model.__name__, value_list=values, mount_point=self._mount_point())
    
    @expose()
    @validate(new_test_form)
    def post(self, *args, **kw):
        log.debug(kw)
        try:
            del kw['sprox_id']
            kw['assignment'] = self.assignment
            if request.teacher:
                kw['teacher'] = request.teacher
            test = Test(**kw)
            DBSession.add(test)
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            log.warning('Error creating event', exc_info=True)
            flash('Error creating event: %s' % e.message, 'error')
            redirect('')
        else:
            flash('Event created', 'ok')
            redirect('')
        #super(TestController, self).post(**kw)
        
    @expose()
    @validate(edit_test_form)
    def put(self, *args, **kw):
        log.debug(args)
        log.debug(kw)
        try:
            kw['id'] = int(kw['id'])
            test = Test.query.get(int(kw['id']))
            kw['assignment'] = self.assignment
            if kw['_timeout']:
                kw['_timeout'] = float(kw['_timeout'])
            else:
                del kw['_timeout']
            if kw['input_data'] is not None:
                kw['input_data'] = kw['input_data'].file.read()
            else:
                del kw['input_data']
            if kw['output_data'] is not None:
                kw['output_data'] = kw['output_data'].file.read()
            else:
                del kw['output_data']
            if request.teacher:
                kw['teacher'] = request.teacher
            for key in kw:
                if hasattr(test, key) and kw[key] != getattr(test, key):
                    setattr(test, key, kw[key])
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            raise
            log.warning('Could not modify test %d', kw['id'], exc_info=True)
            flash('Error modifiying test: %s' % e.message, 'error')
            redirect('edit')
        else:
            flash('Modified test', 'ok')
            redirect('..')
            
