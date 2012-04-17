# -*- coding: utf-8 -*-
'''
Created on 18.03.2012

@author: moschlar
'''

import logging

from tg import request

from repoze.what.predicates import Predicate

from sauce.model import DBSession as Session, User

log = logging.getLogger(__name__)

class has_student(Predicate):
    '''Check user access for given object type and id'''
    
    message = u'YOU SHALL NOT PASS'
    
    def __init__(self, type, id, *args, **kwargs):
        self.type = type
        self.id = id
        try:
            self.obj = Session.query(type).filter_by(id=id).one()
            self.student = self.obj.student
        except:
            self.student = None
        super(has_student, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if request.student == self.student:
            return
        self.unmet()

class is_public(Predicate):
    '''Check if given object is public'''
    
    def __init__(self, obj, *args, **kwargs):
        self.obj = obj
        super(is_public, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if hasattr(self.obj, 'public') and not self.obj.public:
            self.unmet()
        return

class has_teacher(Predicate):
    
    message = u'YOU SHALL NOT PASS'
    
    def __init__(self, type, id, *args, **kwargs):
        self.type = type
        self.id = id
        try:
            self.obj = Session.query(type).filter_by(id=id).one()
            self.teacher = self.obj.teacher
        except:
            self.teacher = None
            super(has_teacher, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if request.teacher == self.teacher:
            return
        self.unmet()
    
class has_teachers(Predicate):
    
    message = u'YOU SHALL NOT PASS'
    
    def __init__(self, type, id, *args, **kwargs):
        self.type = type
        self.id = id
        try:
            self.obj = Session.query(type).filter_by(id=id).one()
            self.teachers = self.obj.teachers
        except:
            self.teacher = None
            super(has_teachers, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if request.teacher in self.teachers:
            return
        self.unmet()
    

class is_teacher(Predicate):
    
    message = u'Only teachers can create judgements'
    
    def evaluate(self, environ, credentials):
        if request.teacher:
            return
        self.unmet()
