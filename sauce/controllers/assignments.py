# -*- coding: utf-8 -*-
"""Assignment controller module"""

import logging

# turbogears imports
from tg import expose, url, flash, redirect, request, abort, tmpl_context as c
#from tg import redirect, validate, flash

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _

from tg.decorators import require
from repoze.what.predicates import not_anonymous

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, Assignment, Submission, Language, Student, Event
from sauce.widgets.submit import submit_form
import transaction
from sauce.controllers.submissions import SubmissionController

log = logging.getLogger(__name__)

class AssignmentController(object):
    
    def __init__(self, assignment_id):
        
        self.assignment_id = assignment_id
        
        try:
            self.assignment = DBSession.query(Assignment).filter(Assignment.id == self.assignment_id).one()
        except NoResultFound:
            abort(404, 'Assignment %d not found' % self.assignment_id, 
                  comment='Assignment %d not found' % self.assignment_id)
        
        self.event = self.assignment.event
        
    @expose('sauce.templates.assignment')
    def index(self, page=1):
        
        try:
            submissions = sorted((s for s in self.assignment.submissions if s.student == request.student), 
                                 key=lambda s: s.date)
        except:
            submissions = []
        
        submissions = Page(submissions, page=page, items_per_page=10)
        
        return dict(page='assignments', event=self.event, assignment=self.assignment, submissions=submissions)
    
    @expose()
    def _lookup(self, action, *args):
        #log.info('%s %s' % (action, args))
        if action == 'submission' or action == 'submit':
            return SubmissionController(assignment_id=self.assignment_id), args
        abort(404)

class AssignmentsController(BaseController):
    
    def __init__(self, event_id=None):
        if event_id:
            self.event_id = event_id
            self.event = DBSession.query(Event).filter_by(id=self.event_id).one()
    
    @expose('sauce.templates.assignments')
    def index(self, page=1):
        
        assignment_query = DBSession.query(Assignment)
        if self.event_id:
            assignment_query = assignment_query.filter(Assignment.event_id == self.event_id)
        assignments = Page(assignment_query, page=page, items_per_page=10)
        
        return dict(page='assignments', event=self.event, assignments=assignments)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return AssignmentController for specified id'''
        
        assignment_id = int(id)
        controller = AssignmentController(assignment_id)
        return controller, args
