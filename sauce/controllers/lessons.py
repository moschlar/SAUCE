# -*- coding: utf-8 -*-
"""Lessons controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, tmpl_context as c, abort, validate, flash, redirect
#from tg import redirect, validate, flash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from repoze.what.authorize import not_anonymous

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Lesson, Team, Student
from sauce.widgets import lesson_table, lesson_filler, team_form

log = logging.getLogger(__name__)

class LessonController(object):
    
    def __init__(self, lesson):
        
        self.lesson = lesson
    
    @expose('sauce.templates.lesson')
    def index(self, **kw):
        c.form = team_form
        return dict(page='lessons', options=kw, lesson=self.lesson, navigation=self.lesson.breadcrumbs)
    
    @expose()
    @validate(team_form, error_handler=index)
    def post(self, **kw):
        log.debug(kw)
        team = Team(lesson=self.lesson, name=kw['name'])
        for stud in kw['students']['grow']:
            if stud['password'] == stud['password_verify']:
                if not stud['email_address']:
                    stud['email_address'] = stud['user_name'] + '@students.uni-mainz.de'
                student = Student(user_name=stud['user_name'], email_address=stud['email_address'],
                                  display_name=stud['display_name'], password=stud['password'])
                team.students.append(student)
            else:
                flash('Passwords for Student %s did not match' % stud['user_name'], 'error')
                redirect('')
        redirect('')
    
class LessonsController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = not_anonymous()
    
    def __init__(self, event):
        self.event = event
    
    @expose('sauce.templates.lessons')
    def index(self):
        c.table = lesson_table
        return dict(page='lessons', value=lesson_filler.get_value())
    
    @expose()
    def _lookup(self, id, *args):
        '''Return EventController for specified url'''
        
        try:
            lesson_id = int(id)
            lesson = DBSession.query(Lesson).filter_by(event_id=self.event.id).filter_by(lesson_id=lesson_id).one()
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        controller = LessonController(lesson)
        return controller, args
