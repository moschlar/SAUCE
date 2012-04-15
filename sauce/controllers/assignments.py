# -*- coding: utf-8 -*-
"""Assignment controller module

@author: moschlar
"""

import logging

# turbogears imports
from tg import expose, request, abort, redirect, url, redirect, validate, flash, tmpl_context as c

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
from sauce.widgets.sproxed import new_assignment_form, edit_assignment_form

log = logging.getLogger(__name__)

class AssignmentController(object):
    
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
        
        return dict(page='assignments', breadcrumbs=self.assignment.breadcrumbs, event=self.event, 
                    assignment=self.assignment, submissions=submissions)
        
    @expose('sauce.templates.form')
    def edit(self, **kw):
        c.form = edit_assignment_form
        return dict(page='assignment', options=kw or self.assignment, child_args=dict(), action=url(self.assignment.url + '/post'))
    
    @expose()
    @validate(edit_assignment_form, error_handler=edit)
    def post(self, **kw):
        log.debug(kw)
        try:
            del kw['sprox_id']
            for key in kw:
                setattr(self.assignment, key, kw[key])
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            log.warning('Error modifying assignment', exc_info=True)
            flash('Error modifying assignment: %s' % e.message, 'error')
            redirect(url(self.assignment.url + '/edit'))
        else:
            flash('Assignment modified', 'ok')
            redirect(url(self.assignment.url))
    
    @expose()
    @require(not_anonymous(msg=u'Only logged in users can submit Submissions'))
    def submit(self):
        '''Create new submission for this assignment'''
        
        submission = Submission(assignment=self.assignment, student=request.student)
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

class AssignmentsController(BaseController):
    
    def __init__(self, sheet):
        
        self.sheet = sheet
        self.event = sheet.event
    
    @expose('sauce.templates.assignments')
    def index(self, page=1):
        ''''Assignment listing page'''
        
        assignments = self.sheet.assignments
        
        return dict(page='assignments', breadcrumbs=self.sheet.breadcrumbs, event=self.sheet.event, assignments=assignments)
    
    @expose('sauce.templates.form')
    def new(self, **kw):
        c.form = new_assignment_form
        if not hasattr(kw, 'teacher'):
            kw['teacher'] = request.teacher
        return dict(page='assignment', options=kw, child_args=dict(), action=url(self.sheet.url + '/assignments/post'))
    
    @expose()
    @validate(new_assignment_form, error_handler=new)
    def post(self, **kw):
        log.debug(kw)
        try:
            del kw['sprox_id']
            assignment = Assignment(sheet=self.sheet, **kw)
            DBSession.add(assignment)
            DBSession.flush()
        except Exception as e:
            DBSession.rollback()
            log.warning('Error creating assignment', exc_info=True)
            flash('Error creating assignment: %s' % e.message, 'error')
            redirect(url(self.event.url + '/assignments'))
        else:
            flash('Assignment created', 'ok')
            redirect(url(assignment.url))
    
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
