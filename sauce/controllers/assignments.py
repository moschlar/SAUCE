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
from sauce.model import DBSession, Assignment, Submission

from sauce.controllers.submissions import SubmissionController, SubmissionsController

log = logging.getLogger(__name__)

class AssignmentController(object):
    
    def __init__(self, assignment):
        
        self.assignment = assignment
        self.sheet = self.assignment.sheet
        self.event = self.sheet.event
        
        self.submissions = SubmissionsController(assignment=self.assignment)
    
    @expose('sauce.templates.assignment')
    def index(self, page=1):
        '''Assignment detail page'''
        
        submissions = Submission.by_assignment_and_student(self.assignment, request.student)
        
        submissions = Page(submissions, page=page, items_per_page=10)
        
        return dict(page='assignments', event=self.event, assignment=self.assignment, submissions=submissions)
    
    @expose()
    def _lookup(self, action, *args):
        #log.info('%s %s' % (action, args))
        if action == 'submission' or action == 'submit':
            return SubmissionController(assignment=self.assignment), args
        abort(404)

class AssignmentsController(BaseController):
    
    def __init__(self, sheet):
        self.sheet = sheet
        self.event = sheet.event
    
    @expose('sauce.templates.assignments')
    def index(self, page=1):
        ''''Assignment listing page'''
        
        assignments = self.sheet.assignments
        
        return dict(page='assignments', event=self.sheet.event, assignments=assignments)
    
    @expose()
    def _lookup(self, assignment_id, *args):
        '''Return AssignmentController for specified assignment_id'''
        
        try:
            assignment_id = int(assignment_id)
            assignment = Assignment.by_assignment_id(assignment_id, self.event)
        except ValueError:
            abort(400)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        controller = AssignmentController(assignment)
        return controller, args
