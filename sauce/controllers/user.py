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
from sqlalchemy.exc import SQLAlchemyError

# project specific imports
from sauce.model import DBSession, User
from sauce.widgets import ProfileForm, SubmissionTable, SubmissionTableFiller

log = logging.getLogger(__name__)


class UserController(TGController):

    allow_only = not_anonymous()

    @expose('sauce.templates.user')
    def index(self):
        #TODO: Ugly.

        memberships = defaultdict(list)

        if request.user:
            memberships['teams'] = request.user.teams
            memberships['lessons'] = request.user._lessons
            memberships['tutored_lessons'] = request.user.tutored_lessons
            #memberships['events'] = request.user.events

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
        teammates.discard(request.user)

        values = SubmissionTableFiller(DBSession).get_value(user_id=request.user.id)

        for teammate in teammates:
            values.extend(SubmissionTableFiller(DBSession).get_value(user_id=teammate.id))

        return dict(page='user', user=request.user, values=values, memberships=memberships)

    @expose('sauce.templates.form')
    def profile(self, **kwargs):
        '''Profile modifying page'''

        c.form = ProfileForm
        return dict(page='user', heading=u'User profile: %s' % request.user.display_name,
                    options=request.user, action=url('/user/post'))

    @validate(ProfileForm, error_handler=profile)
    @expose()
    def post(self, **kwargs):
        '''Process form data into user profile'''

        user = DBSession.merge(request.user)

        try:
            d = User.query.filter_by(email_address=kwargs['email_address']).one()
        except:
            pass
        else:
            if d.user_name != request.user.user_name:
                flash('The email address "%s" is already registered!' % (kwargs['email_address']), 'error')
                redirect(url('/user/profile'))

        try:
            user.first_name = kwargs['first_name']
            user.last_name = kwargs['last_name']
            user.email_address = kwargs['email_address']
            # Only attempt to change password if both values are set
            if kwargs['password_1'] and kwargs['password_1'] == kwargs['password_2']:
                user.password = kwargs['password_1']
            DBSession.flush()
        except SQLAlchemyError:
            DBSession.rollback()
            log.warning('Error modifying profile %s', user.user_name, exc_info=True)
            flash('Error modifying profile', 'error')
        else:
            flash('Profile modified', 'ok')
        finally:
            redirect(url('/user/profile'))
