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
from tgext.crud import CrudRestController
from sprox.fillerbase import TableFiller
from sprox.tablebase import TableBase
from repoze.what.predicates import Any, has_permission
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.auth import has_teachers, has_teacher
from sauce.model import Lesson, Team, Submission, DBSession
from sauce.controllers.crc import (FilteredCrudRestController, TeamsCrudController,
                                   StudentsCrudController, LessonsCrudController)

log = logging.getLogger(__name__)

class SubmissionsController(CrudRestController):
    model = Submission

    class table_type(TableBase):
        __model__ = Submission
        __omit_fields__ = ['__actions__', 'source', 'assignment_id', 'language_id', 'student_id', 'testruns']

    class table_filler_type(TableFiller):
        __model__ = Submission
        __omit_fields__ = ['__actions__', 'source', 'assignment_id', 'language_id', 'student_id', 'testruns']

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
                                                            './%d/submissions' % (self.lesson.lesson_id): 'Submissions',
                                                            },
                                                **kw)
        
        menu_items = {'../%d/' % (self.lesson.lesson_id): 'Lesson',
                      '../%d/teams' % (self.lesson.lesson_id): 'Teams',
                      '../%d/students' % (self.lesson.lesson_id): 'Students',
                      '../%d/submissions' % (self.lesson.lesson_id): 'Submissions',
                     }
        
        self.teams = TeamsCrudController(inject=dict(lesson=self.lesson),
                                         filters=[Team.lesson == self.lesson],
                                         menu_items=menu_items,
                                         **kw)
        self.students = StudentsCrudController(#filters=[Student.id.in_((s.id for t in self.lesson.teams for s in t.students))],
                                               menu_items=menu_items,
                                               **kw)
        
        self.submissions = SubmissionsController(DBSession, menu_items=menu_items, **kw)
        
        # Allow access for event teacher and lesson teacher
        self.allow_only = Any(has_teacher(self.lesson.event),
                              has_teacher(self.lesson),
                              has_permission('manage'),
                              msg=u'You have no permission to manage this Lesson'
                              )
        

class LessonsController(TGController):
    
    def __init__(self, event):
        
        self.event = event
        
        self.allow_only = Any(has_teacher(self.event),
                              has_teachers(self.event),
                              has_permission('manage'),
                              msg=u'You have no permission to manage Lessons for this Event'
                              )
    
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
            flash('Invalid Lesson id: %s' % lesson_id,'error')
            abort(400)
        except NoResultFound:
            flash('Lesson %d not found' % lesson_id,'error')
            abort(404)
        except MultipleResultsFound:
            log.error('Database inconsistency: Lesson %d' % lesson_id, exc_info=True)
            flash('An error occurred while accessing Lesson %d' % lesson_id,'error')
            abort(500)
        
        controller = LessonController(lesson)
        return controller, args

