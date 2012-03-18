# -*- coding: utf-8 -*-
"""Assignment controller module"""

import logging

# turbogears imports
from tg import expose, url, flash, redirect, request, tmpl_context as c
#from tg import redirect, validate, flash

# third party imports
from tg.paginate import Page
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, Assignment, Submission, Language, Student
from sauce.widgets.submit import submit_form
import transaction

log = logging.getLogger(__name__)

class AssignmentController(object):
    
    def __init__(self, assignment_id):
        self.assignment_id = assignment_id
    
    @expose('sauce.templates.assignment')
    def index(self):
        assignment = DBSession.query(Assignment).filter(Assignment.id == self.assignment_id).one()
        return dict(page='assignments', assignment=assignment)
    
    @expose('sauce.templates.submit')
    def submit(self, *args, **kwargs):
        
        assignment = DBSession.query(Assignment).filter(Assignment.id == self.assignment_id).one()
        
        if request.environ['REQUEST_METHOD'] == 'POST':
            
            try:
                assignment_id = int(kwargs['assignment'])
            except:
                assignment_id = self.assignment_id
            else:
                # if assignment in form field differs from assignmend_id from url, there's something wrong
                if assignment_id != self.assignment_id:
                    flash('assignment_id mismatch', 'error')
                    # redirect to self
                    redirect(url(request.environ['PATH_INFO']))
            
            try:
                language_id = int(kwargs['language'])
            except KeyError:
                flash('Could not get language_id', 'error')
                redirect(url(request.environ['PATH_INFO']))
            except ValueError:
                flash('Could not parse language_id', 'error')
                redirect(url(request.environ['PATH_INFO']))
            else:
                language = DBSession.query(Language).filter(Language.id == language_id).one()
            
            if language not in assignment.allowed_languages:
                flash('The Language %s is not allowed for this assignment' % (language), 'error')
                redirect(url(request.environ['PATH_INFO']))
            
            source = ''
            try:
                source = kwargs['source']
                filename = kwargs['filename']
            except:
                pass
            
            try:
                source = kwargs['source_file'].value
                filename = kwargs['source_file'].filename
            except:
                pass
            
            if source.strip() == '':
                flash('Source code is empty, not submitting', 'error')
                redirect(url(request.environ['PATH_INFO']))
            
            #if not filename.endswith(language.extension):
            #    flash('Filename does not match allowed langauge extension', 'error')
            #    redirect(url(request.environ['PATH_INFO']))
            
            try:
                student = DBSession.query(Student).first()
                
                submission = Submission(assignment=assignment, 
                                        language=language, 
                                        student=student,
                                        source=source,
                                        filename=filename)
                
                DBSession.add(submission)
                transaction.commit()
            except Exception as e:
                flash(str(e), 'error')
                redirect(url(request.environ['PATH_INFO']))
            else:
                #if submission not in DBSession:
                #    submission = DBSession.merge(submission)
                flash('Submitted', 'ok')
                redirect(url('/submissions/%d' % submission.id))
            flash('What am I doing here?', 'info')
            redirect(url(request.environ['PATH_INFO']))
        
        # Prepare submit form
        c.form = submit_form
        c.options = dict(assignment=assignment.id, test=True, language='')
        languages = [('', ''), ]
        languages.extend((l.id, l.name) for l in assignment.allowed_languages)
        c.child_args = dict(language=dict(options=languages))
        
        return dict(page='assignments', assignment=assignment)

class AssignmentsController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('sauce.templates.assignments')
    def index(self, page=1):
        
        assignment_query = DBSession.query(Assignment)
        
        assignments = Page(assignment_query, page=page, items_per_page=1)
        
        return dict(page='assignments', assignments=assignments)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return AssignmentController for the specified id'''
        id = int(id)
        assignment = AssignmentController(id)
        return assignment, args