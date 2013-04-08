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
from repoze.what.predicates import Any, not_anonymous, has_permission
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.authz import is_public, has_teacher
from sauce.model import Assignment, Submission, DBSession
from sauce.lib.menu import menu
from sqlalchemy.exc import SQLAlchemyError
from sauce.controllers.lessons import SubmissionsController
try:
    from sauce.controllers.similarity import SimilarityController
except ImportError as e:
    from warnings import warn
    warn('Similarity checking disabled: ' + str(e))
    class SimilarityController(object):
        def __init__(self, *args, **kw):
            pass

log = logging.getLogger(__name__)


class AssignmentController(TGController):

    def __init__(self, assignment):
        self.assignment = assignment
        self.sheet = assignment.sheet
        self.event = self.sheet.event
        c.assignment = self.assignment

        self.allow_only = Any(is_public(self.assignment),
                              has_teacher(self.assignment),
                              has_teacher(self.sheet),
                              has_teacher(self.event),
                              has_permission('manage'),
                              msg=u'This Assignment is not public'
                              )

        self.submissions = SubmissionsController(assignment=self.assignment)
        self.similarity = SimilarityController(assignment=self.assignment)

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.assignment)

    @expose('sauce.templates.assignment')
    def index(self, page=1):
        '''Assignment detail page'''

        if request.user:
            submissions = set(Submission.by_assignment_and_user(self.assignment, request.user).all())
            #submissions = Page(submissions, page=page, items_per_page=10)
            if getattr(request.user, 'teams', False):
                #TODO: Ugly.
                teams = set()
                for lesson in self.assignment.sheet.event.lessons:
                    teams |= set(lesson.teams)
                teams &= set(request.user.teams)
                for member in (member for team in teams for member in team.students):
                    submissions |= set(Submission.by_assignment_and_user(self.assignment, member).all())
            submissions = sorted(list(submissions), key=lambda s: s.modified)
        else:
            submissions = []

        return dict(page='assignments', event=self.event, assignment=self.assignment, submissions=submissions)

    @expose()
    @require(not_anonymous(msg=u'Only logged in users can create Submissions'))
    def submit(self):
        '''Create new submission for this assignment'''
        if not self.assignment.is_active and\
            not request.allowance(self.assignment):
            flash('This assignment is not active, you may not create a submission', 'warning')
            redirect(url(self.assignment.url))

        submission = Submission(assignment=self.assignment, user=request.user,
                                created=datetime.now())
        DBSession.add(submission)
        try:
            DBSession.flush()
        except SQLAlchemyError:
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
    def index(self, page=1):
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
            abort(400)
        except NoResultFound:
            flash('Assignment %d not found' % assignment_id, 'error')
            abort(404)
        except MultipleResultsFound:
            log.error('Database inconsistency: Assignment %d' % assignment_id, exc_info=True)
            flash('An error occurred while accessing Assignment %d' % assignment_id, 'error')
            abort(500)

        controller = AssignmentController(assignment)
        return controller, args
