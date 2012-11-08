# -*- coding: utf-8 -*-
"""Lessons controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, abort, request, tmpl_context as c, flash, TGController
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
from repoze.what.predicates import Any, has_permission
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.auth import has_teachers, has_teacher
from sauce.lib.menu import menu
from sauce.model import Lesson, Team, Submission, Assignment, Sheet, User, DBSession
from sauce.controllers.crc import (FilteredCrudRestController, TeamsCrudController,
                                   StudentsCrudController, LessonsCrudController,
                                   TutorsCrudController)
from sauce.widgets import SubmissionTable, SubmissionTableFiller
from sauce.model.user import lesson_members, team_members
from sqlalchemy.exc import SQLAlchemyError

log = logging.getLogger(__name__)


class SubmissionsController(TGController):

    def __init__(self, *args, **kw):
        # /event/url/submissions
        self.event = kw.get('event', None)
        # /event/url/lesson/id/submissions
        self.lesson = kw.get('lesson', None)
        # /event/url/sheet/id/assignment/id/submissions
        self.assignment = kw.get('assignment', None)
        # /event/url/sheet/id/submissions
        self.sheet = kw.get('sheet', None)
        if self.event:
            pass
        elif self.lesson:
            self.event = self.lesson.event
        elif self.assignment:
            self.event = self.assignment.sheet.event
        elif self.sheet:
            self.event = self.sheet.event
        else:
            log.warn('SubmissionController without any filter')
            flash('You can not view Submissions without any constraint.', 'error')
            abort(400)

        # Allow access for event teacher and lesson teacher
        self.allow_only = Any(has_teacher(self.event),
                              has_teachers(self.event),
                              has_teacher(self.lesson),
                              has_permission('manage'),
                              msg=u'You have no permission to manage this Lesson'
                              )

        self.table = SubmissionTable(DBSession)
        self.table_filler = SubmissionTableFiller(DBSession, lesson=self.lesson)

    def _before(self, *args, **kw):
        '''Prepare tmpl_context with navigation menus'''
        if self.assignment:
            c.sub_menu = menu(self.assignment, True)
        elif self.sheet:
            c.sub_menu = menu(self.sheet, True)
        elif self.event:
            c.sub_menu = menu(self.event, True)

    @expose('sauce.templates.submissions')
    def _default(self, *args, **kw):
        filters = dict(zip(args[::2], args[1::2]))
        real_filters = dict(assignment_id=set(), user_id=set())

        if self.assignment:
            real_filters['assignment_id'] = self.assignment.id
        else:
            sheet = None
            if self.sheet:
                sheet = self.sheet
            elif 'sheet' in filters:
                try:
                    s = int(filters['sheet'])
                    sheet = DBSession.query(Sheet).filter_by(event_id=self.event.id)\
                        .filter_by(sheet_id=s).one()
                except NoResultFound:
                    pass
            if sheet:
                if 'assignment' in filters:
                    try:
                        a = int(filters['assignment'])
                        a_id = DBSession.query(Assignment.id).filter_by(sheet_id=sheet.id).filter_by(assignment_id=a).one().id
                        real_filters['assignment_id'] |= set((a_id, ))
                    except NoResultFound:
                        pass
                else:
                    real_filters['assignment_id'] |= set((a.id for a in sheet.assignments))

        if 'lesson' in filters:
            try:
                l = int(filters['lesson'])
                q1 = DBSession.query(User.id).join(lesson_members).filter_by(lesson_id=l)
                q2 = DBSession.query(User.id).join(team_members).join(Team).filter_by(lesson_id=l)
                students = q1.union(q2)
                real_filters['user_id'] |= set((s.id for s in students))
            except SQLAlchemyError:
                pass
        if 'team' in filters:
            try:
                students = DBSession.query(User.id).join(team_members)\
                    .filter_by(team_id=int(filters['team'])).join(Team)
                if self.lesson:
                    students = students.filter_by(lesson_id=self.lesson.id)
                else:
                    students = students.filter(Team.lesson_id.in_(l.id for l in self.event.lessons))
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
        return dict(page='event', view=None, values=values)


class LessonController(LessonsCrudController):

    model = Lesson
    title = 'Lesson'

    def __init__(self, lesson, **kw):
        self.lesson = lesson

        super(LessonController, self).__init__(inject=dict(tutor=request.user, event=self.lesson.event),
                                               filter_bys=dict(id=self.lesson.id),
                                               menu_items={'./%d/' % (self.lesson.lesson_id): 'Lesson',
                                                           './%d/tutor' % (self.lesson.lesson_id): 'Tutor',
                                                           './%d/teams' % (self.lesson.lesson_id): 'Teams',
                                                           './%d/students' % (self.lesson.lesson_id): 'Students',
                                                           #'./%d/submissions' % (self.lesson.lesson_id): 'Submissions',
                                                           },
                                               btn_new=False, btn_delete=False, path_prefix='.',
                                               **kw)

        menu_items = {'../%d/' % (self.lesson.lesson_id): 'Lesson',
                      '../%d/tutor' % (self.lesson.lesson_id): 'Tutor',
                      '../%d/teams' % (self.lesson.lesson_id): 'Teams',
                      '../%d/students' % (self.lesson.lesson_id): 'Students',
                      #'../%d/submissions' % (self.lesson.lesson_id): 'Submissions',
                     }

        self.teams = TeamsCrudController(inject=dict(lesson=self.lesson),
                                         filters=[Team.lesson == self.lesson],
                                         menu_items=menu_items,
                                         **kw)
        self.students = StudentsCrudController(inject=dict(_lessons=[self.lesson]),
            query_modifier=lambda qry: (qry.join(lesson_members).filter_by(lesson_id=self.lesson.id)
                .union(qry.join(team_members).join(Team).filter_by(lesson_id=self.lesson.id))
                .distinct().order_by(User.id)),
            menu_items=menu_items,
            **kw)
        self.tutor = TutorsCrudController(#filters=[Lesson.tutor == self.lesson.tutor],
            query_modifier=lambda qry: (qry.join(Lesson).filter(Lesson.id == self.lesson.id)
                .order_by(User.id)),
            menu_items=menu_items, btn_new=False, btn_delete=False,
            **kw)

        self.submissions = SubmissionsController(lesson=self.lesson, menu_items=menu_items, **kw)

        # Allow access for event teacher and lesson teacher
        self.allow_only = Any(has_teacher(self.lesson.event),
                              has_teacher(self.lesson),
                              has_permission('manage'),
                              msg=u'You have no permission to manage this Lesson'
                              )

    def _before(self, *args, **kw):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.lesson.event, True)
        super(LessonController, self)._before(*args, **kw)

    @expose()
    def new(self):
        '''No new lessons are to be created.'''
        abort(403)


class LessonsController(TGController):

    def __init__(self, event):
        self.event = event

        self.allow_only = Any(has_teacher(self.event),
                              has_teachers(self.event),
                              has_permission('manage'),
                              msg=u'You have no permission to manage Lessons for this Event'
                              )

    def _before(self, *args, **kw):
        '''Prepare tmpl_context with navigation menus'''
        c.sub_menu = menu(self.event)

    @expose()
    def index(self):
        '''Lesson listing page'''
        return dict(page='lessons', event=self.event)

    @expose()
    def _lookup(self, lesson_id, *args):
        '''Return LessonController for specified lesson_id'''

        try:
            lesson_id = int(lesson_id)
            lesson = Lesson.by_lesson_id(lesson_id, self.event)
        except ValueError:
            flash('Invalid Lesson id: %s' % lesson_id, 'error')
            abort(400)
        except NoResultFound:
            flash('Lesson %d not found' % lesson_id, 'error')
            abort(404)
        except MultipleResultsFound:
            log.error('Database inconsistency: Lesson %d' % lesson_id, exc_info=True)
            flash('An error occurred while accessing Lesson %d' % lesson_id, 'error')
            abort(500)

        controller = LessonController(lesson)
        controller._check_security()
        return controller, args
