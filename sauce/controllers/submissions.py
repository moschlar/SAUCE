# -*- coding: utf-8 -*-
"""Submission controller module

@author: moschlar
"""

import logging
from time import time
from datetime import datetime

from collections import namedtuple

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from difflib import unified_diff, HtmlDiff

# turbogears imports
from tg import expose, request, redirect, url, flash, session, abort, validate, tmpl_context as c, response, TGController
from tg.decorators import require
from tg.paginate import Page

# third party imports
#from tg.i18n import ugettext as _
from repoze.what.predicates import not_anonymous, Any, has_permission
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from chardet import detect

# project specific imports
from sauce.lib.base import BaseController, do_navigation_links
from sauce.lib.auth import has_student, is_teacher, has_teachers, has_user
from sauce.lib.runner import Runner
from sauce.model import DBSession, Assignment, Submission, Language, Testrun, Event, Judgement
from sauce.widgets import submission_form, judgement_form

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
                yield 1, u'<a name="%s-%d" class="%s-%d"">%s</a>' % (s, i, s, i, line)
            else:
                yield 0, line

class ParseError(Exception):
    pass

class SubmissionController(TGController):
    
    allow_only = not_anonymous()
    
    def __init__(self, submission):
        
        self.submission = submission
        self.assignment = submission.assignment
        self.event = self.assignment.event
        
        self.allow_only = Any(has_user(submission),
                              has_teachers(submission.assignment.sheet.event),
                              has_permission('manage'),
                              msg=u'You are not allowed to view this submission'
                              )
        
        c.navigation = do_navigation_links(self.event)
    
    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with breadcrumbs'''
        c.breadcrumbs = self.assignment.breadcrumbs
    
    def parse_kwargs(self, kwargs):
        
        # Get language from kwargs
        try:
            language_id = int(kwargs['language_id'])
        except KeyError:
            raise ParseError('No language selected')
            #redirect(url(request.environ['PATH_INFO']))
        except ValueError:
            raise ParseError('No language selected')
            #redirect(url(request.environ['PATH_INFO']))
        else:
            language = DBSession.query(Language).filter_by(id=language_id).one()
        
        #log.debug('%s %s' % (self.assignment in Session, language in Session))
        #log.debug('language: %s, allowed_languages: %s' % (repr(language), self.assignment.allowed_languages))    
        
        if language not in self.assignment.allowed_languages:
            raise ParseError('The language %s is not allowed for this assignment' % (language))
            #redirect(url(request.environ['PATH_INFO']))
        
        source, filename = u'', u''
        try:
            source = kwargs['source']
            filename = kwargs['filename'] or '%d_%d_%d.%s' % (request.user.id, self.assignment.id, self.submission.id, language.extension_src)
        except KeyError:
            pass
        
        try:
            source = kwargs['source_file'].value
            try:
                source = unicode(source)
            except UnicodeDecodeError as e:
                log.debug('Encoding errors in submission %d', self.submission.id)
                log.debug('%s' % e.message)
                
                try:
                    det = detect(source)
                    log.debug(det)
                    source = unicode(source, encoding=det['encoding'])
                    if det['confidence'] < 0.66:
                        flash('Your submission source code was automatically determined to be '
                              'of encoding ' + det['encoding'] + '. '
                              'Please check for wrongly converted characters!', 'info')
                except UnicodeDecodeError as e:
                    log.debug('%s' % e.message)
                    source = unicode(source, errors='ignore')
                    flash('Your submission source code failed to convert to proper Unicode. '
                          'Please verify your source code for replaced or missing characters. '
                          '(You should not be using umlauts in source code anyway)', 'warning')
            filename = kwargs['source_file'].filename
        except (KeyError, AttributeError):
            pass
        
        if not source.strip():
            raise ParseError('Source code is empty.')
            #redirect(url(request.environ['PATH_INFO']))
        
        return (language, source, filename)
    
    @expose()
    def index(self):
        if request.teacher:
            if self.submission.user == request.user:
                # Teacher on Teachers own submission
                if self.submission.complete:
                    redirect(url(self.submission.url + '/show'))
                else:
                    redirect(url(self.submission.url + '/edit'))
            else:
                # Teacher on Students Submission
                redirect(url(self.submission.url + '/judge'))
        else: 
            # Student on own Submission
            if not self.submission.complete and self.submission.assignment.is_active:
                redirect(url(self.submission.url + '/edit'))
            else:
                redirect(url(self.submission.url + '/show'))
    
    @expose('sauce.templates.submission_show')
    def show(self):
        # TODO: Partial matches
        #hd = HtmlDiff(tabsize, wrapcolumn, linejunk, charjunk)
        #hd.make_table(fromlines, tolines, fromdesc, todesc, context, numlines)
        try:
            lexer = get_lexer_by_name(self.submission.language.lexer_name)
            formatter = MyHtmlFormatter(style='default', linenos=True, prestyles='line-height: 100%', lineanchors='line')
            #c.style = formatter.get_style_defs()
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
                    corrected_source=corrected_source, diff=diff)
    
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
            
            if kwargs.get('grade'):
                self.submission.judgement.grade = float(kwargs['grade'])
            if kwargs.get('comment'):
                self.submission.judgement.comment = kwargs['comment']
            if kwargs.get('corrected_source'):
                self.submission.judgement.corrected_source = kwargs['corrected_source']
            
            # Always rewrite annotations
            self.submission.judgement.annotations = dict()
            for ann in kwargs.get('annotations', []):
                try:
                    line = int(ann['line'])
                except:
                    pass
                else:
                    self.submission.judgement.annotations[line] = ann['comment']
            self.submission.judgement.teacher = request.teacher
            DBSession.add(self.submission.judgement)
            #transaction.commit()
            #self.submission = DBSession.merge(self.submission)
            DBSession.flush()
        
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
            #c.style = formatter.get_style_defs()
            source = highlight(self.submission.source, lexer, formatter)
        except:
            log.info('Could not highlight submission %d', self.submission.id)
            source = self.submission.source
        
        return dict(page='submissions', bread=self.assignment, submission=self.submission,
                    source=source)
    
    #@validate(submission_form)
    @expose('sauce.templates.submission_edit')
    def edit(self, **kwargs):
        
        if request.teacher:
            if self.submission.user == request.user:
                # Teacher on Teachers own submission
                if self.submission.complete:
                    flash('This submission is already submitted, you should not edit it anymore.', 'warning')
                elif not self.assignment.is_active:
                    flash('This assignment is not active, you should not edit this submission anymore.', 'warning')
            else:
                # Teacher on Students Submission
                flash('You are a teacher, you probably don\'t want to edit a student\'s submission. ' +
                      'You probably want to go to the judgement page', 'info')
        else: 
            # Student on own Submission
            if self.submission.complete:
                flash('This submission is already submitted, you can not edit it anymore.', 'warning')
                redirect(url(self.submission.url + '/show'))
            elif not self.assignment.is_active:
                flash('This assignment is not active, you can not edit this submission anymore.', 'warning')
                redirect(url(self.submission.url + '/show'))
                
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
                    DBSession.flush()
                except Exception as e:
                    log.warn('Error deleting submission', exc_info=True)
                else:
                    flash('Resetted', 'ok')
                redirect(url(self.assignment.url))
            else:
                try:
                    (language, source, filename) = self.parse_kwargs(kwargs)
                except ParseError as e:
                    log.debug('parse_kwargs failed', exc_info=True)
                    flash(e.message, 'error')
                else:
                    #self.submission.assignment = self.assignment
                    #if request.student:
                    #    self.submission.student = request.student
                    self.submission.language = language
                    self.submission.source = source
                    self.submission.filename = filename
                    self.submission.modified = datetime.now()
                    
                    DBSession.add(self.submission)
                    #transaction.commit()
                    #self.submission = DBSession.merge(self.submission)
                    DBSession.flush()
            if self.submission.source and not self.submission.complete:
                if test or submit:
                    (compilation, testruns, submitted, result) = self.submission.run_tests(submit)
                    if submit:
                        if submitted:
                            self.submission.complete = True
                            if self.submission.result:
                                flash('Submission was correct, congratulations!', 'ok')
                            else:
                                flash('Submission was not correct, try again!', 'error')
                            redirect(url(self.submission.url + '/show'))
                        else:
                            flash('Your submission did not succeed with the test run you see below. '
                                  'Although your submission is saved, you might want to review it once more.', 'error')
                            #redirect(url(self.submission.url + '/edit'))
                    elif test:
                        if result:
                            #c.child_args['buttons.submit'] = dict(disabled=False)
                            pass
        
        c.options = self.submission
        
        if len(self.assignment.allowed_languages) > 1:
            languages = [(None, '---'), ]
        else:
            languages = []
        languages.extend((l.id, l.name) for l in self.assignment.allowed_languages)
        c.child_args['language_id'] = dict(options=languages)
        
        return dict(page='submissions', bread=self.assignment, event=self.event, assignment=self.assignment, submission=self.submission,
                    compilation=compilation, testruns=testruns)
    
    @expose(content_type='text/plain')
    def download(self, what='submission'):
        '''Download source code'''
        if what not in ('submission', 'judgement'):
            flash('%s is not downloadable' % (what), 'error')
            redirect(url(self.submission.url + '/show'))
        response.headerlist.append(('Content-Disposition', 'attachment;filename=%s' % self.submission.filename))
        if what == 'submission':
            return self.submission.source
        elif what == 'judgement':
            return self.submission.judgement.corrected_source

class SubmissionsController(TGController):
    
    allow_only = not_anonymous(msg=u'Only logged in users may see submissions')
    
    def __init__(self):
        pass
    
    def _before(self, *args, **kwargs):
        '''Prepare tmpl_context with breadcrumbs'''
        #c.breadcrumbs = self.assignment.breadcrumbs
    
    @expose('sauce.templates.submissions')
    def index(self, page=1):
        '''Submission listing page'''
        
        submission_query = Submission.query.filter_by(user_id=request.user.id)
        
        submissions = Page(submission_query, page=page, items_per_page=10)
        
        return dict(page='submissions', submissions=submissions)
    
    @expose()
    def _lookup(self, submission_id, *args):
        '''Return SubmissionController for specified submission_id'''
        
        try:
            submission_id = int(submission_id)
            submission = Submission.query.filter_by(id=submission_id).one()
        except ValueError:
            flash('Invalid Submission id: %s' % submission_id,'error')
            abort(400)
        except NoResultFound:
            flash('Submission %d not found' % submission_id,'error')
            abort(404)
        except MultipleResultsFound:
            log.error('Database inconsistency: Submission %d' % submission_id, exc_info=True)
            flash('An error occurred while accessing Submission %d' % submission_id,'error')
            abort(500)
        
        controller = SubmissionController(submission)
        return controller, args
    
