# -*- coding: utf-8 -*-
"""Tests controller module"""

# turbogears imports
from tg import expose, request
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
from repoze.what import authorize

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, metadata, TestRun, Submission

from sauce.lib.auth import has_student
from repoze.what.predicates import NotAuthorizedError

class TestsController(BaseController):
    
    allow_only = authorize.not_anonymous(msg='You have to be logged in to view events')
    
    @expose('sauce.templates.tests')
    def index(self):
        try:
            request.student
        except:
            raise NotAuthorizedError('You are not a student')
        else:
            testruns = DBSession.query(TestRun).join(Submission).filter(Submission.student_id == request.student.id).all()
        return dict(page='index', testruns=testruns)
