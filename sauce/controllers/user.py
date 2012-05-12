# -*- coding: utf-8 -*-
"""User controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, request, tmpl_context as c, validate, url, flash, redirect, TGController

# third party imports
#from tg.i18n import ugettext as _
from repoze.what.predicates import not_anonymous

# project specific imports
from sauce.model import DBSession
from sauce.widgets import profile_form
from sauce.widgets.sproxed import SubmissionTable, SubmissionTableFiller

log = logging.getLogger(__name__)

class UserController(TGController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = not_anonymous()
    
    @expose('sauce.templates.user')
    def index(self, order_by=None):
        #TODO: Ugly.
        
        student, teacher = dict(), dict()
        
        try:
            submissions = request.user.submissions
        except:
            submissions = []
        
        if request.student:
            ev_le_te = [(team.lesson.event, team.lesson, team) for team in request.student.teams]
            #submissions = request.student.submissions
            student['ev_le_te'] = ev_le_te
            #student['submissions'] = submissions
            student['teams'] = request.student.teams
            student['lessons'] = request.student.lessons
        
        elif request.teacher:
            teacher['events'] = request.teacher.events
            teacher['lessons'] = request.teacher.lessons
#            teacher['submission_table'] = submission_table
#            teacher['submission_values'] = submission_filler.get_value(teacher=request.teacher)
        
        c.table = SubmissionTable(DBSession)
        values = SubmissionTableFiller(DBSession).get_value(user_id=request.user.id)
        
        return dict(page='user', user=request.user, student=student, teacher=teacher,
                    submissions=submissions, values=values)
    
    @expose('sauce.templates.form')
    def profile(self, **kwargs):
        '''Profile modifying page'''
        
        c.form = profile_form
        return dict(page='user', heading=u'User profile: %s' % request.user.display_name, options=request.user, child_args=dict(user_name=dict(disabled=True)), action=url('/user/post'))
    
    @validate(profile_form, error_handler=profile)
    @expose()
    def post(self, **kwargs):
        '''Process form data into user profile'''
        
        try:
            request.user.display_name = kwargs['display_name']
            request.user.email_address = kwargs['email_address']
            # Only attempt to change password if both values are set
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
        
    
