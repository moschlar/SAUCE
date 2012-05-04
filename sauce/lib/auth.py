# -*- coding: utf-8 -*-
'''
Created on 18.03.2012

@author: moschlar
'''

import logging

#TODO: Use environ instead of request if possible
from tg import request

from repoze.what.predicates import Predicate

#TODO: Session shouldn't be needed here
from sauce.model import DBSession as Session, User

log = logging.getLogger(__name__)

class has_student(Predicate):
    '''Check user access for given object type and id'''
    
    message = u'The user must be a student for this %(name)s'
    
    def __init__(self, type, id, *args, **kwargs):
        # TODO: type,id => obj
        self.type = type
        self.name = self.type.__name__
        try:
            self.obj = Session.query(type).filter_by(id=id).one()
            self.student = self.obj.student
        except:
            self.student = None
        super(has_student, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if request.student and request.student == self.student:
            return
        self.unmet()

class has_user(Predicate):
    '''Check user access for given object type and id'''
    
    message = u'The user must be a student for this %(name)s'
    
    def __init__(self, type, id, *args, **kwargs):
        # TODO: type,id => obj
        self.type = type
        self.name = self.type.__name__
        try:
            self.obj = Session.query(type).filter_by(id=id).one()
            self.user = self.obj.user
        except:
            self.user = None
        super(has_user, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if request.user and request.user == self.user:
            return
        self.unmet()

class has_teacher(Predicate):
    
    message = u'The user must be the teacher for this %(name)s'
    
    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        try:
            self.teacher = self.obj.teacher
        except:
            self.teacher = None
        super(has_teacher, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if request.teacher and request.teacher == self.teacher:
            return
        self.unmet()

class has_teachers(Predicate):
    
    message = u'The user must be a teacher for this %(name)s'
    
    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        self.id = id
        try:
            self.teachers = self.obj.teachers
        except:
            self.teachers = []
        try:
            self.teacher = self.obj.teacher
            self.teachers.append(self.teacher)
        except:
            self.teacher = None
        super(has_teachers, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if request.teacher and request.teacher in self.teachers:
            return
        self.unmet()

class is_public(Predicate):
    '''Check if given object is public'''
    
    message = u'This %(name)s must be public'
    
    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        self.name = self.obj.__class__.__name__
        super(is_public, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if hasattr(self.obj, 'public') and not self.obj.public:
            self.unmet()
        return

class is_teacher(Predicate):
    
    message = u'The user must be a teacher'
    
    def evaluate(self, environ, credentials):
        if request.teacher:
            return
        self.unmet()
