# -*- coding: utf-8 -*-
"""Assignment controller module"""

import logging

# turbogears imports
from tg import expose, url
#from tg import redirect, validate, flash

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Assignment

log = logging.getLogger(__name__)

class AssignmentController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.assignments')
    def index(self, page=1):
        
        assignment_query = DBSession.query(Assignment)
        
        assignments = Page(assignment_query, page=page, items_per_page=1)
        
        return dict(page='index', assignments=assignments)
