# -*- coding: utf-8 -*-
"""Lessons controller module

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
try:
    from collections import OrderedDict
except ImportError:  # pragma: no cover
    from ordereddict import OrderedDict

# turbogears imports
from tg import expose, abort, tmpl_context as c, flash, TGController
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
import status
from repoze.what.predicates import Any, has_permission
from sqlalchemy import union
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.authz import user_is_in
from sauce.lib.menu import menu
from sauce.model import Lesson, Team, Assignment, Sheet, User, DBSession
from sauce.controllers.crc import (TeamsCrudController, StudentsCrudController,
    LessonsCrudController, TutorsCrudController)
from sauce.widgets import SubmissionTable, SubmissionTableFiller
from sauce.model.user import lesson_members, team_members
from sauce.model.event import lesson_tutors
from sqlalchemy.exc import SQLAlchemyError
from sauce.controllers.crc.base import CrudIndexController

log = logging.getLogger(__name__)


class SubmissionsController(TGController):

    def __init__(self, *args, **kwargs):
        # /event/url/submissions
        self.event = kwargs.get('event', None)
        # /event/url/lesson/id/submissions
        self.lesson = kwargs.get('lesson', None)
        # /event/url/sheet/id/assignment/id/submissions
        self.assignment = kwargs.get('assignment', None)
        # /event/url/sheet/id/submissions
        self.sheet = kwargs.get('sheet', None)
        if self.event:
            pass
        elif self.lesson:
            self.event = self.lesson.event
        elif self.assignment:
            self.event = self.assignment.sheet.event
        elif self.sheet:
            self.event = self.sheet.event
        else:  # pragma: no cover
            log.warn('SubmissionController without any filter')
            flash('You can not view Submissions without any constraint.', 'error')
            abort(status.HTTP_400_BAD_REQUEST)

        # Allow access for event teacher and lesson teacher
        self.allow_only = Any(
            user_is_in('teachers', self.event),
            user_is_in('tutors', self.lesson),
            has_permission('manage'),
            msg=u'You have no permission to manage this Lesson'
        )

        self.table = SubmissionTable(DBSession)
        self.table_filler = SubmissionTableFiller(DBSession, lesson=self.lesson)

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        if self.assignment:
            c.sub_menu = menu(self.assignment)
        elif self.sheet:
            c.sub_menu = menu(self.sheet)
        elif self.event:
            c.sub_menu = menu(self.event)

    @expose('sauce.templates.submissions')
    def _default(self, *args, **kwargs):
        # TODO: This filtering really needs to be rewritten!
        filters = dict(zip(args[::2], args[1::2]))
        real_filters = dict(assignment_id=set(), user_id=set())

        if self.assignment:
            real_filters['assignment_id'] = set((self.assignment.id, ))
        else:
            sheet = None
            if self.sheet:
                sheet = self.sheet
            elif 'sheet' in filters:
                try:
                    s = int(filters['sheet'])
                    sheet = (DBSession.query(Sheet).filter_by(event_id=self.event.id)
                        .filter_by(sheet_id=s).one())
                except NoResultFound:
                    pass
            if sheet:
                if 'assignment' in filters:
                    try:
                        a = int(filters['assignment'])
                        a_id = (DBSession.query(Assignment.id).filter_by(sheet_id=sheet.id)
                            .filter_by(assignment_id=a).one().id)
                        real_filters['assignment_id'] |= set((a_id, ))
                    except NoResultFound:
                        pass
                else:
                    real_filters['assignment_id'] |= set((a.id for a in sheet.assignments))

        if self.event:
            # Dirty, dirty hack to properly filter assignments by event
            if real_filters['assignment_id']:
                # Only allow filters by assignments from the set event
                real_filters['assignment_id'] &= set((a.id for s in self.event.sheets for a in s.assignments))
            else:
                # Simply filter by assignments for this event
                real_filters['assignment_id'] = set((a.id for s in self.event.sheets for a in s.assignments))

        if 'lesson' in filters:
            try:
                l = int(filters['lesson'])
                q1 = DBSession.query(User.id).join(lesson_members).filter_by(lesson_id=l).order_by(None)
                q2 = DBSession.query(User.id).join(team_members).join(Team).filter_by(lesson_id=l).order_by(None)
                students = DBSession.query(User.id).select_entity_from(union(q1, q2)).order_by(User.id)
                real_filters['user_id'] |= set((s.id for s in students))
            except SQLAlchemyError:
                pass
        if 'team' in filters:
            try:
                students = (DBSession.query(User.id).join(team_members)
                    .filter_by(team_id=int(filters['team'])).join(Team))
                if self.lesson:
                    students = students.filter_by(lesson_id=self.lesson.id)
                else:
                    #students = students.filter(Team.lesson_id.in_(l.id for l in self.event.lessons))
                    students = students.join(Team.lesson).filter_by(event_id=self.event.id)
                real_filters['user_id'] |= set((s.id for s in students))
            except SQLAlchemyError:
                pass
        if 'user' in filters:
            try:
                user_id = DBSession.query(User.id).filter_by(id=int(filters['user'])).one().id
                real_filters['user_id'] |= set((user_id, ))
            except NoResultFound:
                pass

        # Cleanup filters for performancy
        definite_filters = dict()
        for (k, v) in real_filters.iteritems():
            if v:
                if isinstance(v, (list, tuple, set)) and len(v) == 1:
                    definite_filters[k] = v.pop()
                else:
                    definite_filters[k] = v

        c.table = self.table
        values = self.table_filler.get_value(filters=definite_filters)
        return dict(page='event', view=None, values=values,
            filters=filters, real_filters=real_filters, definite_filters=definite_filters)


class LessonController(CrudIndexController):

    title = 'Lesson'

    def __init__(self, lesson, **kwargs):
        self.lesson = lesson

        menu_items = OrderedDict((
            ('./lessons/', 'Lesson'),
            ('./tutors/', 'Tutor'),
            ('./teams/', 'Teams'),
            ('./students/', 'Students'),
            #('./submissions/', 'Submissions'),
        ))
        self.menu_items = menu_items

        super(LessonController, self).__init__(**kwargs)

        self.lessons = LessonsCrudController(
            # inject=dict(tutor=request.user, event=self.lesson.event),  # No new lesson to be created
            query_modifier=lambda qry: qry.filter_by(id=self.lesson.id),
            query_modifiers={
                # Tutors can only delegate ownership to other tutors
                #'tutor': lambda qry: qry.filter(User.id.in_((t.id for t in self.lesson.event.tutors))),
                'tutor': lambda qry: qry.join(User.tutored_lessons).filter_by(event_id=self.lesson.event.id)
            },
            allow_new=False, allow_delete=False,
            menu_items=self.menu_items,
            **kwargs)
        self.students = StudentsCrudController(
            inject=dict(_lessons=[self.lesson]),
            query_modifier=lambda qry: qry.select_entity_from(union(
                    qry.join(lesson_members).filter_by(lesson_id=self.lesson.id).order_by(None),
                    qry.join(team_members).join(Team).filter_by(lesson_id=self.lesson.id).order_by(None),
                )).order_by(User.id),
            query_modifiers={
                'teams': lambda qry: qry.filter_by(lesson_id=self.lesson.id),
                '_lessons': lambda qry: qry.filter_by(id=self.lesson.id),
            },
            menu_items=self.menu_items,
            allow_delete=False,
            hints=dict(lesson=self.lesson, event=self.lesson.event),
            **kwargs)
        self.teams = TeamsCrudController(
            # inject=dict(lesson=self.lesson),  # Field shows only one value
            query_modifier=lambda qry: qry.filter_by(lesson_id=self.lesson.id),
            query_modifiers={
                #'members': lambda qry: qry.filter(User.id.in_((u.id for u in self.lesson.event.members))),
                'members': lambda qry: qry.select_entity_from(union(
                        qry.join(lesson_members).join(Lesson).filter_by(event_id=self.lesson.event.id).order_by(None),
                        qry.join(team_members).join(Team).join(Team.lesson).filter_by(event_id=self.lesson.event.id).order_by(None),
                    )).order_by(User.id),
                'lesson': lambda qry: qry.filter_by(id=self.lesson.id),
            },
            menu_items=self.menu_items,
            hints=dict(lesson=self.lesson, event=self.lesson.event),
            **kwargs)
        self.tutors = TutorsCrudController(
            query_modifier=lambda qry: (qry.join(lesson_tutors).filter_by(lesson_id=self.lesson.id)
                .order_by(User.id)),
            query_modifiers={
                'tutored_lessons': lambda qry: qry.filter(Lesson.event == self.lesson.event),
            },
            menu_items=self.menu_items, allow_new=False, allow_delete=False,
            hints=dict(lesson=self.lesson, event=self.lesson.event),
            **kwargs)

        self.submissions = SubmissionsController(lesson=self.lesson, menu_items=self.menu_items, **kwargs)

        # Allow access for event teacher and lesson teacher
        self.allow_only = Any(
            user_is_in('teachers', self.lesson.event),
            user_is_in('tutors', self.lesson),
            has_permission('manage'),
            msg=u'You have no permission to manage this Lesson'
        )

    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.lesson.event, True)
        super(LessonController, self)._before(*args, **kwargs)

    @expose()
    def new(self, *args, **kwargs):
        '''No new lessons are to be created.'''
        abort(status.HTTP_403_FORBIDDEN)


class LessonsController(TGController):

    def __init__(self, event):
        self.event = event

        self.allow_only = Any(
            user_is_in('teachers', self.event),
            user_is_in('tutors', self.event),
            has_permission('manage'),
            msg=u'You have no permission to manage Lessons for this Event'
        )

#     def _before(self, *args, **kwargs):
#         '''Prepare tmpl_context with navigation menus'''
#         c.sub_menu = menu(self.event)
#
#     @expose()
#     def index(self, *args, **kwargs):
#         '''Lesson listing page'''
#         return dict(page='lessons', event=self.event)

    @expose()
    def _lookup(self, lesson_id, *args):
        '''Return LessonController for specified lesson_id'''

        try:
            lesson_id = int(lesson_id)
            lesson = Lesson.by_lesson_id(lesson_id, self.event)
        except ValueError:
            flash('Invalid Lesson id: %s' % lesson_id, 'error')
            abort(status.HTTP_400_BAD_REQUEST)
        except NoResultFound:
            flash('Lesson %d not found' % lesson_id, 'error')
            abort(status.HTTP_404_NOT_FOUND)
        except MultipleResultsFound:  # pragma: no cover
            log.error('Database inconsistency: Lesson %d', lesson_id, exc_info=True)
            flash('An error occurred while accessing Lesson %d' % lesson_id, 'error')
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

        controller = LessonController(lesson)
        controller._check_security()
        return controller, args
