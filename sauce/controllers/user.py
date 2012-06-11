# -*- coding: utf-8 -*-
"""User controller module

@author: moschlar
"""

import logging
from collections import defaultdict

# turbogears imports
from tg import expose, request, tmpl_context as c, validate, url, flash, redirect, TGController

# third party imports
#from tg.i18n import ugettext as _
from repoze.what.predicates import not_anonymous

# project specific imports
from sauce.model import DBSession
from sauce.widgets import ProfileForm, SubmissionTable, SubmissionTableFiller

log = logging.getLogger(__name__)

class UserController(TGController):

    allow_only = not_anonymous()

    @expose('sauce.templates.user')
    def index(self):
        #TODO: Ugly.
        
        memberships = defaultdict(list)
        
        if request.student:
            memberships['teams'] = request.student.teams
            memberships['lessons'] = request.student._lessons
        elif request.teacher:
            memberships['lessons'] = request.teacher.lessons
            memberships['events'] = request.teacher.events
        
        c.table = SubmissionTable(DBSession)
        
#        events = set((event for event in memberships['events']))
#        events |= set((lesson.event for lesson in memberships['lessons']))
#        events |= set((team.lesson.event for team in memberships['teams']))
#        
#        for event in events:
#            for sheet in event.sheets:
#                for assignment in sheet.assignments:
#                    pass
        
        teammates = set()
        for team in memberships['teams']:
            teammates |= set(team.students)
        teammates.discard(request.student)
        
        values = SubmissionTableFiller(DBSession).get_value(user_id=request.user.id)
        
        for teammate in teammates:
            values.extend(SubmissionTableFiller(DBSession).get_value(user_id=teammate.id))
        
        return dict(page='user', user=request.user, values=values, memberships=memberships)
    
    @expose('sauce.templates.form')
    def profile(self, **kwargs):
        '''Profile modifying page'''
        
        c.form = ProfileForm
        return dict(page='user', heading=u'User profile: %s' % request.user.display_name,
                    options=request.user, child_args=dict(user_name=dict(disabled=True)), action=url('/user/post'))
    
    @validate(ProfileForm, error_handler=profile)
    @expose()
    def post(self, **kwargs):
        '''Process form data into user profile'''
        
        try:
            request.user.first_name = kwargs['first_name']
            request.user.last_name = kwargs['last_name']
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
        
    
