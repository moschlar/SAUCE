# -*- coding: utf-8 -*-
"""EventAdmin controller module

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
from tg import request

# third party imports
#from tg.i18n import ugettext as _
from repoze.what.predicates import Any, has_permission
from sqlalchemy import or_, union

# project specific imports
from sauce.lib.authz import user_is_in
from sauce.model import Lesson, Team, User, Assignment, Test, Event, NewsItem
from sauce.controllers.crc.base import CrudIndexController
from sauce.controllers.crc import *
from sauce.model.user import lesson_members, team_members, event_members
from sauce.model.event import lesson_tutors

log = logging.getLogger(__name__)


class EventAdminController(CrudIndexController):
    ''''''

    title = 'Event'

    def __init__(self, event, **kwargs):
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
            ('./newsitems/', 'NewsItems'),
        ))
        self.menu_items = menu_items

        super(EventAdminController, self).__init__(**kwargs)

        self.events = EventsCrudController(
            inject=dict(teacher=request.user),
            query_modifier=lambda qry: qry.filter_by(id=self.event.id),
            menu_items=self.menu_items,
            allow_new=False, allow_delete=False,
            **kwargs)

        self.lessons = LessonsCrudController(
            inject=dict(event=self.event),
            query_modifier=lambda qry: qry.filter_by(event_id=self.event.id),
            query_modifiers={
                # Disabled so that the teacher can assign any users as tutors
                #'tutor': lambda qry: qry.filter(User.id.in_((t.id for t in self.event.tutors))),
                'teams': lambda qry: qry.join(Team.lesson).filter_by(event_id=self.event.id),
            },
            menu_items=self.menu_items,
            **kwargs)

        self.teams = TeamsCrudController(
            #query_modifier=lambda qry: qry.filter(Team.lesson_id.in_((l.id for l in self.event.lessons))),
            query_modifier=lambda qry: qry.join(Team.lesson).filter_by(event_id=self.event.id),
            query_modifiers={
                'lesson': lambda qry: qry.filter_by(event_id=self.event.id),
                # Disabled so that the teacher can assign any users as members
                #'members': lambda qry: qry.filter(User.id.in_((u.id for u in self.lesson.event.members))),
            },
            menu_items=self.menu_items,
            hints=dict(event=self.event),
            **kwargs)

        self.students = StudentsCrudController(
            query_modifier=lambda qry: qry.select_entity_from(union(
                    qry.join(event_members).join(Event)
                        .filter_by(id=self.event.id).order_by(None),
                    qry.join(lesson_members).join(Lesson)
                        .filter_by(event_id=self.event.id).order_by(None),
                    qry.join(team_members).join(Team).join(Lesson)
                        .filter_by(event_id=self.event.id).order_by(None),
                )).order_by(User.user_name),
            query_modifiers={
                #'teams': lambda qry: qry.filter(Team.lesson_id.in_((l.id for l in self.event.lessons))),
                'teams': lambda qry: qry.join(Team.lesson).filter_by(event_id=self.event.id),
                '_lessons': lambda qry: qry.filter_by(event_id=self.event.id),
            },
            menu_items=self.menu_items,
            hints=dict(event=self.event),
            **kwargs)

        self.tutors = TutorsCrudController(
            query_modifier=lambda qry: (qry.join(lesson_tutors).join(Lesson)
                .filter_by(event_id=self.event.id).order_by(User.id)),
            query_modifiers={
                'tutored_lessons': lambda qry: qry.filter_by(event_id=self.event.id),
            },
            menu_items=self.menu_items,
            hints=dict(event=self.event),
            **kwargs)

        self.sheets = SheetsCrudController(
            inject=dict(event=self.event, _teacher=request.user),
            query_modifier=lambda qry: qry.filter_by(event_id=self.event.id),
            menu_items=self.menu_items,
            allow_copy=True,
            **kwargs)

        self.assignments = AssignmentsCrudController(
            inject=dict(_teacher=request.user),
            query_modifier=lambda qry: qry.join(Assignment.sheet).filter_by(event_id=self.event.id),
            query_modifiers={
                'sheet': lambda qry: qry.filter_by(event_id=self.event.id),
            },
            menu_items=self.menu_items,
            **kwargs)

        self.tests = TestsCrudController(
            inject=dict(user=request.user),
            query_modifier=lambda qry: (qry.join(Test.assignment).join(Assignment.sheet)
                .filter_by(event_id=self.event.id)),
            query_modifiers={
                'assignment': lambda qry: qry.join(Assignment.sheet).filter_by(event_id=self.event.id),
            },
            menu_items=self.menu_items,
            **kwargs)

        self.newsitems = NewsItemController(
            inject=dict(user=request.user),
            query_modifier=lambda qry: qry.filter(or_(NewsItem.event == None, NewsItem.event == self.event)),
            query_modifiers={
                'event': lambda qry: qry.filter_by(id=self.event.id),
            },
            menu_items=self.menu_items,
            **kwargs)

        self.allow_only = Any(
            user_is_in('teachers', self.event),
            has_permission('manage'),
            msg=u'You have no permission to manage this Event'
        )
