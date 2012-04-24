# -*- coding: utf-8 -*-
"""Assignment controller module

@author: moschlar
"""

import logging
from datetime import datetime

# turbogears imports
from tg import expose, request, abort, redirect, url, redirect, validate, flash, tmpl_context as c
from tg.controllers import TGController

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _

from tg.decorators import require
from repoze.what.predicates import Any, not_anonymous

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import transaction

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import Assignment, Submission, DBSession

from sauce.controllers.submissions import SubmissionController, SubmissionsController

from sauce.lib.auth import is_public

log = logging.getLogger(__name__)

class AssignmentController(TGController):
    
    def __init__(self, assignment):
        
        self.assignment = assignment
        self.sheet = self.assignment.sheet
        self.event = self.sheet.event
        
        self.submissions = SubmissionsController(assignment=self.assignment)
        
        #self.allow_only = Any(is_public(self.assignment))
    
    @expose('sauce.templates.assignment')
    def index(self, page=1):
        '''Assignment detail page'''
        
        if request.student:
            submissions = Submission.by_assignment_and_student(self.assignment, request.student)
            submissions = Page(submissions, page=page, items_per_page=10)
        else:
            submissions = []
        
        return dict(page='assignments', bread=self.assignment, event=self.event, 
                    assignment=self.assignment, submissions=submissions)
        
    
    @expose()
    @require(not_anonymous(msg=u'Only logged in users can submit Submissions'))
    def submit(self):
        '''Create new submission for this assignment'''
        
        submission = Submission(assignment=self.assignment, student=request.student, created=datetime.now())
        DBSession.add(submission)
        try:
            DBSession.flush()
        except:
            DBSession.rollback()
            redirect(url(self.assignment.url))
        else:
            redirect(url(submission.url))

    @expose()
    @require(not_anonymous(msg=u'Only logged in users can submit Submissions'))
    def _lookup(self, action, *args):
        '''Return SubmissionController for this Assignment'''
        
        if action == 'submission' or action == 'submit':
            return SubmissionController(assignment=self.assignment), args
        abort(404)

class AssignmentsController(TGController):
    
    def __init__(self, sheet):
        
        self.sheet = sheet
        self.event = sheet.event
    
    @expose('sauce.templates.assignments')
    def index(self, page=1):
        ''''Assignment listing page'''
        
        assignments = self.sheet.assignments
        
        return dict(page='assignments', bread=self.assignment, event=self.sheet.event, assignments=assignments)
    
    @expose()
    def _lookup(self, assignment_id, *args):
        '''Return AssignmentController for specified assignment_id'''
        
        try:
            assignment_id = int(assignment_id)
            assignment = Assignment.by_assignment_id(assignment_id, self.sheet)
        except ValueError:
            abort(400)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        controller = AssignmentController(assignment)
        return controller, args
