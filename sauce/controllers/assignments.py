# -*- coding: utf-8 -*-
"""Assignment controller module

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
from datetime import datetime

# turbogears imports
from tg import expose, request, abort, url, redirect, tmpl_context as c, flash, TGController
from tg.decorators import require
#from tg.i18n import ugettext as _

# third party imports
import status
from repoze.what.predicates import Any, not_anonymous, has_permission
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import SQLAlchemyError

# project specific imports
from sauce.lib.authz import user_is_in, is_public
from sauce.model import Assignment, Submission, DBSession
from sauce.lib.menu import menu
from sauce.controllers.lessons import SubmissionsController
from sauce.widgets import SubmissionTable, SubmissionTableFiller, SourceDisplay

try:
    from sauce.controllers.similarity import SimilarityController
except ImportError as e:  # pragma: no cover
    from warnings import warn
    warn('Similarity checking disabled: ' + str(e), RuntimeWarning)

    class SimilarityController(object):
        def __init__(self, *args, **kwargs):
            pass

log = logging.getLogger(__name__)


class AssignmentController(TGController):

    def __init__(self, assignment):
        self.assignment = assignment
        self.sheet = assignment.sheet
        self.event = self.sheet.event
        c.assignment = self.assignment

        self.allow_only = Any(
            is_public(self.assignment),
            user_is_in('teachers', self.event),
            user_is_in('tutors', self.event),
            has_permission('manage'),
            msg=u'This Assignment is not public'
        )

        self.submissions = SubmissionsController(assignment=self.assignment)
        self.similarity = SimilarityController(assignment=self.assignment)

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.assignment)

        mode = self.assignment.allowed_languages[0].lexer_name \
            if len(self.assignment.allowed_languages) == 1 else ''
        c.source_display = SourceDisplay(mode=mode)

    @expose('sauce.templates.assignment')
    def index(self, page=1, *args, **kwargs):
        '''Assignment detail page'''

        values = []

        if request.user:
            c.table = SubmissionTable(DBSession)

            values = SubmissionTableFiller(DBSession).get_value(
                assignment_id=self.assignment.id,
                user_id=request.user.id,
            )

            teams = set()
            for lesson in self.assignment.sheet.event.lessons:
                teams |= set(lesson.teams)
            teams &= set(request.user.teams)

            teammates = set()
            for team in teams:
                teammates |= set(team.members)
            teammates.discard(request.user)

            for teammate in teammates:
                values.extend(SubmissionTableFiller(DBSession).get_value(
                    assignment_id=self.assignment.id,
                    user_id=teammate.id,
                ))

        return dict(page='assignments', event=self.event, assignment=self.assignment, values=values)

    @expose()
    @require(not_anonymous(msg=u'Only logged in users can create Submissions'))
    def submit(self, *args, **kwargs):
        '''Create new submission for this assignment'''
        if 'manage' not in request.permissions and \
                request.user not in set(self.event.members) | set(self.event.tutorsandteachers):
            abort(status.HTTP_403_FORBIDDEN)
        if (not self.assignment.is_active and
                not request.allowance(self.assignment)):
            flash('This assignment is not active, you may not create a submission', 'warning')
            redirect(url(self.assignment.url))

        submission = Submission(
            assignment=self.assignment,
            filename=self.assignment.submission_filename or None,
            source=self.assignment.submission_template or None,
            language=self.assignment.allowed_languages[0] if self.assignment.allowed_languages else None,
            user=request.user,
            created=datetime.now(),
            modified=datetime.now(),
        )
        DBSession.add(submission)
        try:
            DBSession.flush()
        except SQLAlchemyError:  # pragma: no cover
            DBSession.rollback()
            log.warn('Error creating new submission', exc_info=True)
            flash('Error creating new submission', 'error')
            redirect(url(self.assignment.url))
        else:
            redirect(url(submission.url + '/edit'))


class AssignmentsController(TGController):

    def __init__(self, sheet):
        self.sheet = sheet
        self.event = sheet.event

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.sheet)

    @expose('sauce.templates.assignments')
    def index(self, page=1, *args, **kwargs):
        ''''Assignment listing page'''
        assignments = self.sheet.assignments
        return dict(page='assignments', event=self.sheet.event,
                    sheet=self.sheet, assignments=assignments)

    @expose()
    def _lookup(self, assignment_id, *args):
        '''Return AssignmentController for specified assignment_id'''

        try:
            assignment_id = int(assignment_id)
            assignment = Assignment.by_assignment_id(assignment_id, self.sheet)
        except ValueError:
            flash('Invalid Assignment id: %s' % assignment_id, 'error')
            abort(status.HTTP_400_BAD_REQUEST)
        except NoResultFound:
            flash('Assignment %d not found' % assignment_id, 'error')
            abort(status.HTTP_404_NOT_FOUND)
        except MultipleResultsFound:  # pragma: no cover
            log.error('Database inconsistency: Assignment %d', assignment_id, exc_info=True)
            flash('An error occurred while accessing Assignment %d' % assignment_id, 'error')
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

        controller = AssignmentController(assignment)
        return controller, args
