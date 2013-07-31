# -*- coding: utf-8 -*-
"""User controller module

@author: moschlar
"""
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
from collections import defaultdict

# turbogears imports
from tg import expose, request, tmpl_context as c, validate, url, flash, redirect, TGController, config

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

        options = request.user
        if config.get('externalauth', False):
            options.disable_submit = True
            flash('Profile changes are not possible because external authentication is used!', 'error')
        else:
            options.disable_submit = False

        return dict(page='user', heading=u'User profile: %s' % request.user.display_name,
                    options=options, action=url('/user/post'))

    @validate(ProfileForm, error_handler=profile)
    @expose()
    def post(self, **kwargs):
        '''Process form data into user profile'''

        if config.get('externalauth', False):
            flash('Profile changes are not possible because external authentication is used!', 'error')
            redirect(url('/user/profile'))

        user = DBSession.merge(request.user)

#        try:
#            d = User.query.filter_by(email_address=kwargs['email_address']).one()
#        except:
#            pass
#        else:
#            if d.user_name != request.user.user_name:
#                flash('The email address "%s" is already registered!' % (kwargs['email_address']), 'error')
#                redirect(url('/user/profile'))

        try:
            user._display_name = kwargs.get('display_name', '')
#            user.first_name = kwargs['first_name']
#            user.last_name = kwargs['last_name']
            user.email_address = kwargs.get('email_address', '')
            # Only attempt to change password if both values are set
            if kwargs.get('password_1', None) and \
                    kwargs.get('password_1', None) == kwargs.get('password_2', None):
                user.password = kwargs.get('password_1', '')
            DBSession.flush()
        except SQLAlchemyError:
            DBSession.rollback()
            log.warning('Error modifying profile %s', user.user_name, exc_info=True)
            flash('Error modifying profile', 'error')
        except:
            log.warning('Error modifying profile %s', user.user_name, exc_info=True)
            flash('Error modifying profile', 'error')
        else:
            flash('Profile modified', 'ok')
        finally:
            redirect(url('/user/profile'))
