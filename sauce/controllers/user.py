# -*- coding: utf-8 -*-
"""User controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, request, tmpl_context as c, validate
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
from repoze.what import predicates, authorize

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession
from sauce.widgets import profile_form

import transaction

log = logging.getLogger(__name__)

class UserController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.user')
    def index(self):
        
        if request.student:
            ev_le_te = [(team.lesson.event, team.lesson, team) for team in request.student.teams]
            
        
        return dict(page='user', user=request.user, student=dict(ev_le_te=ev_le_te), teacher=dict())
    
    @validate(profile_form)
    @expose('sauce.templates.profile')
    def profile(self, **kwargs):
        log.debug(kwargs)
        
        if request.environ['REQUEST_METHOD'] == 'POST':
            user = DBSession.merge(request.user)
            user.display_name = kwargs['display_name']
            user.email_address = kwargs['email_address']
            if kwargs['password_1'] and kwargs['password_1'] == kwargs['password_2']:
                user.password = kwargs['password_1']
            transaction.commit()
            request.user = user
        
        c.form = profile_form
        return dict(page='user', user=request.user)
    
    @expose()
    def submissions(self):
        return dict()
    
    @expose()
    def submissions(self):
        return dict()
    
    @expose()
    def submissions(self):
        return dict()
    
