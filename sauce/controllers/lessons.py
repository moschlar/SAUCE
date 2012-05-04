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
from sauce.model import Lesson, Team, Submission, Student, DBSession
from sauce.controllers.crc import (FilteredCrudRestController, TeamsCrudController,
                                   StudentsCrudController, LessonsCrudController)
from sqlalchemy.sql.expression import or_
from sauce.lib.helpers import link

log = logging.getLogger(__name__)

def _actions(filler, subm):
    result = link(u'Show', subm.url + '/show')
    if request.teacher:
        result += ' ' + link(u'Judge', subm.url + '/judge')
    return result

class SubmissionsController(TGController):
    
    class table_type(TableBase):
        __model__ = Submission
        __omit_fields__ = ['source', 'assignment_id', 'language_id', 'user_id',
                           'testruns', 'filename']
        __add_fields__ = {'result': None, 'judgement': None, 'grade': None}

    class table_filler_type(TableFiller):
        __model__ = Submission
        __omit_fields__ = ['source', 'assignment_id', 'language_id', 'user_id',
                           'testruns', 'filename']
        __add_fields__ = {'result': None, 'judgement': None, 'grade': None}
        __actions__ = _actions
        
        def result(self, obj):
            if obj.result:
                return u'<span class="green" style="color:green;">Success</a>'
            else:
                return u'<span class="red" style="color:red;">Failed</a>'
        
        def judgement(self, obj):
            if obj.judgement:
                return u'<a class="green" style="color:green; text-decoration:underline;" href="%s/judge">Yes</a>' % (obj.url)
            else:
                return u'<a class="red" style="color:red; text-decoration:underline;" href="%s/judge">No</a>' % (obj.url)
        
        def grade(self, obj):
            if obj.judgement and obj.judgement.grade:
                return unicode(obj.judgement.grade)
            else:
                return u''
        
        #def id(self, obj):
        #    return u'<a style="text-decoration:underline;" href="%s/judge">Submission %d</a>' % (obj.url, obj.id)

    def __init__(self, lesson, *args, **kw):
        
        self.lesson = lesson
        
        self.table = self.table_type(DBSession)
        self.table_filler = self.table_filler_type(DBSession)
    
    @expose('sauce.templates.submissions')
    def index(self, view='by_sheets'):
        if view == 'by_sheets':
            pass
        elif view == 'by_teams':
            pass
        elif view == '':
            pass
        
        submissions = Submission.query.filter(Submission.user_id.in_(s.id for s in self.lesson.students))
        
        c.table = self.table
        
        return dict(page='event', view=view, submissions=submissions,
                    value_list=self.table_filler.get_value())

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
        self.students = StudentsCrudController(inject=dict(lessons=[self.lesson]),
                                               filters=[Student.id.in_(s.id for s in self.lesson.students)],
                                               menu_items=menu_items,
                                               **kw)
        
        self.submissions = SubmissionsController(self.lesson,
                                                 DBSession, menu_items=menu_items, **kw)
        
        # Allow access for event teacher and lesson teacher
        self.allow_only = Any(has_teacher(self.lesson.event),
                              has_teacher(self.lesson),
                              has_permission('manage'),
                              msg=u'You have no permission to manage this Lesson'
                              )
        
    @expose()
    def new(self):
        abort(403)

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

