# -*- coding: utf-8 -*-
"""Assignment controller module"""

import logging

# turbogears imports
from tg import expose, url, tmpl_context as c
#from tg import redirect, validate, flash

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Assignment
from sauce.widgets.submit import submit_form

log = logging.getLogger(__name__)

class AssignmentController(object):
    
    def __init__(self, assignment_id):
        self.assignment_id = assignment_id
    
    @expose('sauce.templates.assignment')
    def index(self):
        assignment = DBSession.query(Assignment).filter(Assignment.id == self.assignment_id).one()
        return dict(assignment=assignment)
    
    @expose('sauce.templates.submit')
    def submit(self, *args, **kwargs):
        print args
        print kwargs
        assignment = DBSession.query(Assignment).filter(Assignment.id == self.assignment_id).one()
        c.form = submit_form
        return dict(assignment=assignment)

class AssignmentsController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.assignments')
    def index(self, page=1):
        
        assignment_query = DBSession.query(Assignment)
        
        assignments = Page(assignment_query, page=page, items_per_page=1)
        
        return dict(page='index', assignments=assignments)
    
    @expose()
    def _lookup(self, id, *args):
        id = int(id)
        assignment = AssignmentController(id)
        return assignment, args