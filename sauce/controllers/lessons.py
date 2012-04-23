# -*- coding: utf-8 -*-
"""Lessons controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, abort, request
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.model import Lesson, Team, Student, Event
from sauce.controllers.crc import FilteredCrudRestController, TeamsCrudController, StudentsCrudController, LessonsCrudController
from sauce.lib.auth import has_teachers, has_teacher
from repoze.what.predicates import Any, has_permission
from tg.controllers.tgcontroller import TGController
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

log = logging.getLogger(__name__)


class LessonController(LessonsCrudController):
    
    model = Lesson
    title = 'Lesson'
    
    def __init__(self, lesson, **kw):
        
        self.lesson = lesson
        
        super(LessonController, self).__init__(inject=dict(teacher=request.teacher, event=self.lesson.event),
                                                filter_bys=dict(event_id=self.lesson.event_id), 
                                                menu_items={'./%d/' % (self.lesson.lesson_id): 'Lesson',
                                                            './%d/teams' % (self.lesson.lesson_id): 'Teams',
                                                            './%d/students' % (self.lesson.lesson_id): 'Students',
                                                            #'./%d/submissions' % (self.lesson.lesson_id): 'Submissions',
                                                            },
                                                **kw)
        
        self.teams = TeamsCrudController(filters=[Team.lesson == self.lesson],
                                         menu_items={'../%d/' % (self.lesson.lesson_id): 'Lesson',
                                                     '../%d/teams' % (self.lesson.lesson_id): 'Teams',
                                                     '../%d/students' % (self.lesson.lesson_id): 'Students',
                                                     #'../%d/submissions' % (self.lesson.lesson_id): 'Submissions',
                                                     },
                                         **kw)
        self.students = StudentsCrudController(filters=[Student.id.in_((s.id for t in self.lesson.teams for s in t.students))],
                                               menu_items={'../%d/' % (self.lesson.lesson_id): 'Lesson',
                                                           '../%d/teams' % (self.lesson.lesson_id): 'Teams',
                                                           '../%d/students' % (self.lesson.lesson_id): 'Students',
                                                           #'../%d/submissions' % (self.lesson.lesson_id): 'Submissions',
                                                           },
                                               **kw)
        
        # Allow access for event teacher and lesson teacher
        self.allow_only = Any(has_teacher(Event, self.lesson.event.id), has_teacher(Lesson, self.lesson.id), has_permission('manage'))
    

class LessonsController(TGController):
    
    def __init__(self, event):
        
        self.event = event
        self.allow_only = Any(has_teacher(Event, self.event.id), has_teachers(Event, self.event.id), has_permission('manage'))
    
    @expose('sauce.templates.sheets')
    def index(self):
        '''Lesson listing page'''
        
        return dict(page='lessons', bread=self.event, event=self.event)

    @expose()
    def _lookup(self, lesson_id, *args):
        '''Return LessonController for specified lesson_id'''
        
        try:
            lesson_id = int(lesson_id)
            lesson = Lesson.by_lesson_id(lesson_id, self.event)
        except ValueError:
            abort(400)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        controller = LessonController(lesson)
        return controller, args

