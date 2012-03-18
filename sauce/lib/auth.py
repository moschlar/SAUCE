'''
Created on 18.03.2012

@author: moschlar
'''

import logging

from repoze.what.predicates import Predicate

log = logging.getLogger(__name__)

class is_enrolled(Predicate):
    message = 'Student must be enrolled for Event'
    
    def __init__(self, *args, **kwargs):
        #self.student = student
        log.debug(args)
        log.debug(kwargs)
        super(is_enrolled, self).__init__(kwargs)
    
    def evaluate(self, environ, credentials):
        log.debug(environ)
        log.debug(credentials)
        # credentials['repoze.what.userid']
        # credentials['groups']
        # credentials['permissions']
        