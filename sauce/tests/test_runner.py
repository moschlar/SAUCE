'''

THIS TESTCASE IS BROKEN ATM!

Created on 15.03.2012

@author: moschlar
'''
from unittest import TestCase
from sauce.tests import *

from sauce.model import Assignment, Submission, Language, Compiler, Interpreter, Test, Student, DBSession as Session
import transaction
from sauce.lib.runner import run

# Create an empty database before we start our tests for this module
def setup():
    """Function called by nose on module load"""
    setup_db()

# Tear down that database
def teardown():
    """Function called by nose after all tests in this module ran"""
    teardown_db()

class TestRunner(TestCase):
    '''Perform simple "Hello World!" tests on the runner library'''
    
    def setUp(self):
        '''Set up test with a simple assignment and test case'''
        
        self.a = Assignment('Assignment A', 'Write a program that says "Hello World!"', timeout=1)
        #self.a.id = 1
        Session.add(self.a)
        
        self.t = Test('stdin_stdout', self.a, output='Hello World!')
        Session.add(self.t)
        
        self.s = Student("Stu Dent")
        Session.add(self.s)
        
        transaction.commit()
    
    def test_run_c(self):
        '''Test runner with a C submission'''
        
        self.cc = Compiler('GCC', '/usr/bin/gcc', '{srcfile} -o {objfile}', 5)
        #self.cc.id = 1
        Session.add(self.cc)
        self.lc = Language('C', 'c', compiler=self.cc)
        #self.lc.id = 1
        Session.add(self.lc)
        
        self.sc = Submission(self.a ,self.lc, self.s)
        self.sc.source = r'''
#include <stdio.h>

int main(void) {
printf("Hello World!\n");
return 0;
}
        '''
        #self.sc.id = 1
        Session.add(self.sc)
        transaction.commit()
        self.assertTrue(run(self.sc), 'C test failed')
        
    def test_run_python(self):
        '''Test runner with a python submission'''
        
        self.ip = Interpreter('Python 2.7', '/usr/bin/python2.7', '{srcfile}')
        #self.ip.id = 1
        Session.add(self.ip)
        self.lp = Language('Python', 'py', interpreter=self.ip)
        #self.lp.id = 2
        Session.add(self.lp)
        self.sp = Submission(self.a, self.lp, self.s)
        self.sp.source = r'''
print "Hello World!"
        '''
        #self.sp.id = 2
        Session.add(self.sp)
        transaction.commit()
        self.assertTrue(run(self.sp), 'Python test failed')
    
    def test_run_timeout(self):
        '''Test runner with an always reached timeout value'''
        
        self.ip = Interpreter('Python 2.7', '/usr/bin/python2.7', '{srcfile}')
        #self.ip.id = 1
        Session.add(self.ip)
        self.lp = Language('Python', 'py', interpreter=self.ip)
        #self.lp.id = 2
        Session.add(self.lp)
        self.sp = Submission(self.a, self.lp, self.s)
        self.sp.source = r'''
import time
time.sleep(2)
print "Hello World!"
        '''
        #self.sp.id = 2
        Session.add(self.sp)
        transaction.commit()
        self.assertFalse(run(self.sp), 'Timeout test failed')
