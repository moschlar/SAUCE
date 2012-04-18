# -*- coding: utf-8 -*-
"""Submission controller module

@author: moschlar
"""

import logging
from time import time

from collections import namedtuple

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from difflib import unified_diff, HtmlDiff

# turbogears imports
from tg import expose, request, redirect, url, flash, session, abort, validate, tmpl_context as c
#from tg import redirect, validate, flash
from tg.paginate import Page
from tg.controllers import TGController

# third party imports
#from tg.i18n import ugettext as _
from repoze.what import predicates, authorize

from sqlalchemy.orm import joinedload #, joinedload_all, subqueryload, immediateload
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import transaction

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, Assignment, Submission, Language, Testrun, Event

from sauce.lib.runner import Runner

from sauce.widgets import submission_form, judgement_form
from sauce.lib.auth import has_student, is_teacher
from repoze.what.predicates import not_anonymous
from sauce.widgets.judgement import JudgementForm
from sauce.model.submission import Judgement
from tg.decorators import require

log = logging.getLogger(__name__)
results = namedtuple('results', ('result', 'ok', 'fail', 'total'))


class MyHtmlFormatter(HtmlFormatter):
    '''Create lines that have unique name tags to allow highlighting'''
    
    def _wrap_lineanchors(self, inner):
        s = self.lineanchors
        i = 0
        for t, line in inner:
            if t:
                i += 1
                yield 1, '<a name="%s-%d" class="%s-%d"">%s</a>' % (s, i, s, i, line)
            else:
                yield 0, line

class SubmissionController(BaseController):
    
    allow_only = authorize.not_anonymous()
    
    def __init__(self, assignment=None, submission=None):
        
        if bool(assignment) == bool(submission):
            raise Exception('Both constructor values set, that should never happen')
        
        self.submission_id = None
        
        if assignment:
            self.assignment = assignment
            self.submission = Submission()
        
        if submission:
            self.submission = submission
            self.assignment = self.submission.assignment
            
            #self.allow_only = has_student(type=Submission, id=submission.id, 
            #                          msg='You may only view your own submissions')
        
        self.event = self.assignment.event
    
    def parse_kwargs(self, kwargs):
        
        # Get language from kwargs
        try:
            language_id = int(kwargs['language_id'])
        except KeyError:
            raise Exception('No language selected')
            #redirect(url(request.environ['PATH_INFO']))
        except ValueError:
            raise Exception('No language selected')
            #redirect(url(request.environ['PATH_INFO']))
        else:
            language = DBSession.query(Language).filter_by(id=language_id).one()
        
        #log.debug('%s %s' % (self.assignment in Session, language in Session))
        #log.debug('language: %s, allowed_languages: %s' % (repr(language), self.assignment.allowed_languages))    
        
        if language not in self.assignment.allowed_languages:
            raise Exception('The language %s is not allowed for this assignment' % (language))
            #redirect(url(request.environ['PATH_INFO']))
        
        source = ''
        try:
            source = kwargs['source']
            filename = kwargs['filename'] or '%d_%d.%s' % (request.student.id, self.assignment.id, language.extension_src)
        except:
            pass
        
        try:
            source = kwargs['source_file'].value
            filename = kwargs['source_file'].filename
        except:
            pass
        
        if source.strip() == '':
            raise Exception('Source code is empty, not submitting')
            #redirect(url(request.environ['PATH_INFO']))
        
        return (language, source, filename)
    
        
    @expose()
    def index(self):
        if not self.submission.complete and self.submission.assignment.is_active:
            redirect(url(self.submission.url + '/edit'))
        else:
            redirect(url(self.submission.url + '/show'))
        
    
    @expose('sauce.templates.submission_show')
    def show(self):
        #hd = HtmlDiff(tabsize, wrapcolumn, linejunk, charjunk)
        #hd.make_table(fromlines, tolines, fromdesc, todesc, context, numlines)
        try:
            lexer = get_lexer_by_name(self.submission.language.lexer_name)
            formatter = MyHtmlFormatter(style='default', linenos=True, prestyles='line-height: 100%', lineanchors='line')
            c.style = formatter.get_style_defs()
            source = highlight(self.submission.source, lexer, formatter)
        except:
            log.info('Could not highlight submission %d', self.submission.id)
            source = self.submission.source
        
        if self.submission.judgement and self.submission.judgement.corrected_source:
            corrected_source = highlight(self.submission.judgement.corrected_source, lexer, formatter)
            udiff = unified_diff(self.submission.source.splitlines(True), self.submission.judgement.corrected_source.splitlines(True), 'your source', 'corrected source')
            diff = highlight(''.join(udiff), get_lexer_by_name('diff'), formatter)
        else:
            corrected_source = None
            diff = None
        
        return dict(page='submissions', bread=self.assignment, 
                    event=self.event, submission=self.submission, source=source, 
                    corrected_source = corrected_source, diff=diff)
    
    @require(is_teacher())
    @validate(judgement_form)
    @expose('sauce.templates.submission_judge')
    def judge(self, **kwargs):
        
        if request.environ['REQUEST_METHOD'] == 'POST':
            log.debug(kwargs)
            
            test = kwargs.get('buttons.test')
            submit = kwargs.get('buttons.submit')
            reset = kwargs.get('buttons.reset')
            
            if not self.submission.judgement:
                self.submission.judgement = Judgement()
            self.submission.teacher = request.teacher
            if kwargs.get('comment'):
                self.submission.judgement.comment = kwargs['comment']
            if kwargs.get('corrected_source'):
                self.submission.judgement.corrected_source = kwargs['corrected_source']
            
            # Always rewrite annotations
            self.submission.judgement.annotations = dict()
            for ann in kwargs.get('annotations'):
                try:
                    line = int(ann['line'])
                except:
                    pass
                else:
                    self.submission.judgement.annotations[line] = ann['comment']
            self.submission.judgement.teacher = request.teacher
            DBSession.add(self.submission.judgement)
            transaction.commit()
            self.submission = DBSession.merge(self.submission)
        
        c.form = judgement_form
        c.options = dict()
        if self.submission.judgement:
            a = self.submission.judgement.annotations
            c.options['annotations'] = [dict(line=i, comment=a[i]) for i in sorted(a)]
            c.options['comment'] = self.submission.judgement.comment
            c.options['corrected_source'] = self.submission.judgement.corrected_source
            c.options['grade'] = self.submission.judgement.grade
        
        c.child_args = dict()
        
        try:
            lexer = get_lexer_by_name(self.submission.language.lexer_name)
            formatter = MyHtmlFormatter(style='default', linenos=True, prestyles='line-height: 100%', lineanchors='line')
            c.style = formatter.get_style_defs()
            source = highlight(self.submission.source, lexer, formatter)
        except:
            log.info('Could not highlight submission %d', self.submission.id)
            source = self.submission.source
        
        return dict(page='submissions', bread=self.assignment, submission=self.submission,
                    source=source)
    
    #@validate(submission_form)
    @expose('sauce.templates.submission_edit')
    def edit(self, **kwargs):
        if self.submission.complete:
            flash('This submission is already submitted, you can not edit it anymore.', 'info')
            redirect(url(self.submission.url+'/show'))
        elif not self.assignment.is_active:
            flash('This assignment is not active, you can not edit it anymore.', 'info')
            redirect(url(self.submission.url+'/show'))
        
        # Some initialization
        c.form = submission_form
        c.options = dict()
        c.child_args = dict()
        compilation = None
        testruns = []
        submit = None
        
        #log.debug(kwargs)
        
        if request.environ['REQUEST_METHOD'] == 'POST':
            
            test = kwargs.get('buttons.test')
            submit = kwargs.get('buttons.submit')
            reset = kwargs.get('buttons.reset')
            
            if reset:
                try:
                    DBSession.delete(self.submission)
                except Exception as e:
                    log.warn('Error deleting submission', exc_info=True)
                else:
                    flash('Resetted', 'ok')
                redirect(url(self.assignment.url))
            else:
                try:
                    (language, source, filename) = self.parse_kwargs(kwargs)
                except Exception as e:
                    flash(str(e), 'error')
                else:
                    self.submission.assignment = self.assignment
                    self.submission.student = request.student
                    self.submission.language = language
                    self.submission.source = source
                    self.submission.filename = filename
                    
                    DBSession.add(self.submission)
                    transaction.commit()
                    self.submission = DBSession.merge(self.submission)
                    
            if self.submission.source and not self.submission.complete:
                if test or submit:
                    (compilation, testruns, submitted, self.result) = self.submission.run_tests(submit)
                    if submit:
                        self.submission.complete = True
                        if self.submission.result:
                            flash('Submission is correct', 'ok')
                        else:
                            flash('Submission is not correct', 'error')
                        redirect(url(self.submission.url + '/show'))
        
        c.options = self.submission
        
        if len(self.assignment.allowed_languages) > 1:
            languages = [(None, '---'), ]
        else:
            languages = []
        languages.extend((l.id, l.name) for l in self.assignment.allowed_languages)
        c.child_args['language_id'] = dict(options=languages)
        
        return dict(page='submissions', bread=self.assignment, event=self.event, assignment=self.assignment, submission=self.submission,
                    compilation=compilation, testruns=testruns)
    

class SubmissionsController(BaseController):
    
    allow_only = not_anonymous(msg=u'Only logged in users may see submissions')
    
    def __init__(self, assignment=None):
        
        self.assignment = assignment
        
        if self.assignment:
            self.sheet = self.assignment.sheet
            self.event = self.sheet.event
        
    @expose('sauce.templates.submissions')
    def index(self, page=1):
        
        if self.assignment:
            submission_query = Submission.by_assignment_and_student(self.assignment, request.student)
        else:
            submission_query = Submission.query.filter_by(student_id=request.student.id)
        
        submissions = Page(submission_query, page=page, items_per_page=10)
        
        return dict(page='submissions', submissions=submissions)
    
    @expose()
    def _lookup(self, id, *args):
        '''Return SubmissionController for specified submission_id'''
        
        # Redirect to /submissions/{id}
        #if len(request.environ['PATH_INFO'].split('/')) > 4:
        #    redirect(url('/submissions/%s' % id))
        
        try:
            id = int(id)
            submission = Submission.query.filter_by(id=id).one()
        except ValueError:
            abort(400)
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(500)
        
        controller = SubmissionController(submission=submission)
        return controller, args
    
