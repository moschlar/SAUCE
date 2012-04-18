# -*- coding: utf-8 -*-
"""User controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, request, tmpl_context as c, validate, url, flash, redirect
from tg.controllers import TGController

# third party imports
#from tg.i18n import ugettext as _
from repoze.what import predicates, authorize

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession
from sauce.widgets import profile_form

import transaction

log = logging.getLogger(__name__)

class UserController(TGController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.user')
    def index(self):
        
        student, teacher = dict(), dict()
        
        if request.student:
            ev_le_te = [(team.lesson.event, team.lesson, team) for team in request.student.teams]
            submissions = request.student.submissions
            student['evl_le_te'] = ev_le_te
            student['submissions'] = submissions
        
        elif request.teacher:
            teacher['events'] = request.teacher.events
            teacher['lessons'] = request.teacher.lessons
        
        return dict(page='user', user=request.user, student=student, teacher=teacher)
    
    @expose('sauce.templates.form')
    def profile(self, **kwargs):
        '''Profile modifying page'''
        #log.debug(kwargs)
        
        c.form = profile_form
        return dict(page='user', heading=u'User profile: %s' % request.user.display_name, options=request.user, child_args=dict(user_name=dict(disabled=True)), action=url('/user/post'))
    
    @validate(profile_form, error_handler=profile)
    @expose()
    def post(self, **kwargs):
        '''Process form data into user profile'''
        try:
            request.user.display_name = kwargs['display_name']
            request.user.email_address = kwargs['email_address']
            if kwargs['password_1'] and kwargs['password_1'] == kwargs['password_2']:
                request.user.password = kwargs['password_1']
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            log.warning('Error modifying profile', exc_info=True)
            flash('Error modifying profile: %s' % e.message, 'error')
        else:
            flash('Profile modified', 'ok')
        finally:
            redirect(url('/user/profile'))
        
    
