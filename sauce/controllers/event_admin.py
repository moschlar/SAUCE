# -*- coding: utf-8 -*-
"""EventAdmin controller module

@author: moschlar
"""

import logging
from collections import OrderedDict

# turbogears imports
from tg import expose, request, tmpl_context as c

# third party imports
#from tg.i18n import ugettext as _
from repoze.what.predicates import Any, has_permission

# project specific imports
from sauce.lib.auth import has_teacher
from sauce.model import Lesson, Team, User, Sheet, Assignment, Test, Event, NewsItem, DBSession
from sauce.controllers.crc.base import CrudIndexController
from sauce.controllers.crc import *
from sauce.model.user import lesson_members, team_members
import inspect
from sqlalchemy import or_

log = logging.getLogger(__name__)


class EventAdminController(CrudIndexController):
    ''''''

    title = 'Event'

    def __init__(self, event, **kw):
        self.event = event

        menu_items = OrderedDict((
            ('./events/', 'Event'),
            ('./tutors/', 'Tutors'),
            ('./lessons/', 'Lessons'),
            ('./teams/', 'Teams'),
            ('./students/', 'Students'),
            ('./sheets/', 'Sheets'),
            ('./assignments/', 'Assignments'),
            ('./tests/', 'Tests'),
            ))
        self.menu_items = menu_items

        super(EventAdminController, self).__init__(**kw)

        self.events = EventsCrudController(
            inject=dict(teacher=request.user),
            query_modifier=lambda qry: qry.filter_by(id=self.event.id),
            menu_items=self.menu_items,
            allow_new=False, allow_delete=False,
            **kw)

        self.lessons = LessonsCrudController(
            inject=dict(event=self.event),
            query_modifier=lambda qry: qry.filter_by(event_id=self.event.id),
            query_modifiers={
                # Disabled so that the teacher can assign any users as tutors
                #'tutor': lambda qry: qry.filter(User.id.in_((t.id for t in self.event.tutors))),
                },
            menu_items=self.menu_items,
            **kw)

        self.teams = TeamsCrudController(
            #query_modifier=lambda qry: qry.filter(Team.lesson_id.in_((l.id for l in self.event.lessons))),
            query_modifier=lambda qry: qry.join(Team.lesson).filter_by(event_id=self.event.id),
            query_modifiers={
                'lesson': lambda qry: qry.filter_by(event_id=self.event.id),
                # Disabled so that the teacher can assign any users as members
                #'members': lambda qry: qry.filter(User.id.in_((u.id for u in self.lesson.event.members))),
                },
            menu_items=self.menu_items,
            **kw)

        self.students = StudentsCrudController(
            query_modifier=lambda qry: (qry.join(lesson_members).join(Lesson)
                #.filter(Lesson.id.in_(l.id for l in self.event.lessons))
                .filter_by(event_id=self.event.id)
                .union(qry.join(team_members).join(Team).join(Team.lesson)
                    .filter_by(event_id=self.event.id))
                .distinct().order_by(User.id)),
            query_modifiers={
                #'teams': lambda qry: qry.filter(Team.lesson_id.in_((l.id for l in self.event.lessons))),
                'teams': lambda qry: qry.join(Team.lesson).filter_by(event_id=self.event.id),
                '_lessons': lambda qry: qry.filter_by(event_id=self.event.id),
                },
            menu_items=self.menu_items,
            **kw)

        self.tutors = TutorsCrudController(
            query_modifier=lambda qry: (qry.join(Lesson).filter_by(event_id=self.event.id).order_by(User.id)),
            menu_items=self.menu_items,
            **kw)

        self.sheets = SheetsCrudController(
            inject=dict(event=self.event, _teacher=request.user),
            query_modifier=lambda qry: qry.filter_by(event_id=self.event.id),
            menu_items=self.menu_items,
            **kw)

        self.assignments = AssignmentsCrudController(
            inject=dict(_teacher=request.user),
          query_modifier=lambda qry: qry.join(Assignment.sheet).filter_by(event_id=self.event.id),
            query_modifiers={
                'sheet': lambda qry: qry.filter_by(event_id=self.event.id),
                },
          menu_items=self.menu_items,
          **kw)

        self.tests = TestsCrudController(
            inject=dict(user=request.user),
            query_modifier=lambda qry: (qry.join(Test.assignment).join(Assignment.sheet)
                .filter_by(event_id=self.event.id)),
            query_modifiers={
                'assignment': lambda qry: qry.join(Assignment.sheet).filter_by(event_id=self.event.id),
                },
            menu_items=self.menu_items,
            **kw)

        self.newsitems = NewsItemController(
            inject=dict(user=request.user),
            query_modifier=lambda qry: qry.filter(or_(NewsItem.event == None, NewsItem.event == self.event)),
            query_modifiers={
                'event': lambda qry: qry.filter_by(id=self.event.id),
                },
            menu_items=self.menu_items,
            **kw)

        self.allow_only = Any(
            has_teacher(self.event),
            has_permission('manage'),
            msg=u'You have no permission to manage this Event')
