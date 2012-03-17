# -*- coding: utf-8 -*-
"""Submission controller module"""

# turbogears imports
from tg import expose
#from tg import redirect, validate, flash

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Submission


class SubmissionController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.submission')
    def index(self, page=1):
        
        submission_query = DBSession.query(Submission)
        
        submission = Page(submission_query, page=page, items_per_page=1)
        
        return dict(page='index', submission=submission)