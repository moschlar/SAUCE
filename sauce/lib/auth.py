'''
Created on 18.03.2012

@author: moschlar
'''

import logging

from tg import request

from repoze.what.predicates import Predicate

from sauce.model import DBSession as Session, User

log = logging.getLogger(__name__)

class is_enrolled(Predicate):
    message = u'Student must be enrolled for Event'
    
    def __init__(self, *args, **kwargs):
        #self.student = student
        #log.debug(args)
        #log.debug(kwargs)
        super(is_enrolled, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        #log.debug(environ)
        #log.debug(credentials)
        # credentials['repoze.what.userid']
        # credentials['groups']
        # credentials['permissions']
        self.unmet()
        

class has_student(Predicate):
    '''Check user access for given object type and id'''
    
    message = u'YOU SHALL NOT PASS'
    
    def __init__(self, type, id, *args, **kwargs):
        self.type = type
        self.id = id
        self.obj = Session.query(type).filter_by(id=id).one()
        try:
            self.student = self.obj.student
        except:
            self.student = None
        super(has_student, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        if request.student == self.student:
            return
        self.unmet()
