# -*- coding: utf-8 -*-
"""Events controller module

@author: moschlar
"""

import logging
from datetime import datetime

# turbogears imports
from tg import expose, abort, require, tmpl_context as c, validate, redirect, flash, url, request
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
from repoze.what.predicates import not_anonymous, has_permission

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.base import BaseController
import sauce.model as model
from sauce.model import DBSession, Event, Lesson, Team, Student
#from sauce.controllers.assignments import AssignmentsController
#from sauce.controllers.submissions import SubmissionsController
#from sauce.controllers.scores import ScoresController
from sauce.controllers.sheets import SheetsController
from sauce.controllers.lessons import LessonsController

from sauce.controllers.crc import FilteredCrudRestController

from sauce.lib.auth import has_teacher
from sauce.widgets.sproxed import new_event_form, edit_event_form
from sauce.lib.helpers import link

log = logging.getLogger(__name__)

class EventController(object):
    
    def __init__(self, event):
        
        self.event = event
        self.sheets = SheetsController(event=event)
        self.lessons = LessonsController(event=event)
        
    @expose('sauce.templates.event')
    def index(self):
        '''Event details page'''
        
        return dict(page='events', navigation=self.event.breadcrumbs+[link(u'Lessons', self.event.url+'/lessons')], event=self.event)
    
    @expose()
    @require(not_anonymous(msg=u'Only logged in users can enroll for events'))
    def enroll(self):
        '''Event enrolling page'''
        
        password = self.event.password
        
        return dict(page='events', enroll=True)
    
    
    @expose('sauce.templates.form')
    #@require(has_permission('edit_event'))
    def edit(self, **kw):
        '''Event edit page'''
        c.form = edit_event_form
        
        return dict(page='events', options=kw or self.event, child_args=dict(), action=url(self.event.url+'/post'))
    
    @validate(edit_event_form, error_handler=edit)
    @expose()
    #@require(has_permission('edit_event'))
    def post(self, **kw):
        '''Process form data into self.event'''
        log.debug(kw)
        try:
            del kw['sprox_id']
            #kw['start_time'] = datetime.strptime(kw['start_time'], '%Y-%m-%d %H:%M:%S')
            #kw['end_time'] = datetime.strptime(kw['end_time'], '%Y-%m-%d %H:%M:%S')
            try:
                kw['teacher'] = model.Teacher.query.get(int(kw['teacher']))
            except:
                kw['teacher'] = None
            kw['teachers'] = [model.Teacher.query.get(int(t)) for t in kw['teachers']]
            for key in kw:
                setattr(self.event, key, kw[key])
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            log.warning('Error modifying event', exc_info=True)
            flash('Error modifying event: %s' % e.message, 'error')
            redirect(url(self.event.url+'/edit'))
        else:
            flash('Event modified', 'ok')
            redirect(url(self.event.url))
    
class EventsController(BaseController):
    
    @expose('sauce.templates.events')
    def index(self, page=1):
        '''Event listing page'''
        
        events = Page(Event.current_events(), page=page, items_per_page=10)
        future_events = Page(Event.future_events(), page=page, items_per_page=10)
        previous_events = Page(Event.previous_events(), page=page, items_per_page=10)
        
        return dict(page='events', events=events, previous_events=previous_events, future_events=future_events)
    
    @expose('sauce.templates.form')
    #@require(has_permission('edit_event'))
    def new(self, **kw):
        '''Event creation page'''
        c.form = new_event_form
        if not hasattr(kw, 'teacher'):
            kw['teacher'] = request.teacher
        return dict(page='events', options=kw, child_args=dict(), action=url('/events/post'))
    
    @validate(new_event_form, error_handler=new)
    @expose()
    #@require(has_permission('edit_event'))
    def post(self, **kw):
        '''Process form data into new event'''
        log.debug(kw)
        try:
            del kw['sprox_id']
            #kw['start_time'] = datetime.strptime(kw['start_time'], '%Y-%m-%d %H:%M:%S')
            #kw['end_time'] = datetime.strptime(kw['end_time'], '%Y-%m-%d %H:%M:%S')
            try:
                kw['teacher'] = model.Teacher.query.get(int(kw['teacher']))
            except:
                kw['teacher'] = None
            kw['teachers'] = [model.Teacher.query.get(int(t)) for t in kw['teachers']]
            event = Event(**kw)
            DBSession.add(event)
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            log.warning('Error creating event', exc_info=True)
            flash('Error creating event: %s' % e.message, 'error')
            redirect(url('/events'))
        else:
            flash('Event created', 'ok')
            redirect(url(event.url))
    
    @expose()
    def _lookup(self, url, *args):
        '''Return EventController for specified url'''
        
        try:
            event = Event.by_url(url)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        controller = EventController(event)
        return controller, args
