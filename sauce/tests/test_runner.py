'''

THIS TESTCASE IS BROKEN ATM!

Created on 15.03.2012

@author: moschlar
'''
from unittest import TestCase
from sauce.tests import *

from sauce.model import Assignment, Submission, Language, Compiler, Interpreter, Test, Student

from sauce.lib.runner import Runner

class TestRunner(TestCase):
    '''Perform simple "Hello World!" tests on the runner library'''
    
    def setUp(self):
        '''Set up test with a simple assignment and test case'''
        
        self.a = Assignment('Assignment A', 'Write a program that says "Hello World!"', timeout=1)
        self.a.id = 1
        
        self.t = Test('stdin_stdout', self.a, output='Hello World!')
        
        self.s = Student('Stu Dent')
        
        self.cc = Compiler('GCC', '/usr/bin/gcc', '{srcfile} -o {objfile}', 5)
        self.cc.id = 1
        
        self.lc = Language('C', 'c', compiler=self.cc)
        self.lc.id = 1
        
        
        self.ip = Interpreter('Python 2.7', '/usr/bin/python2.7', '{srcfile}')
        self.ip.id = 1
        
        self.lp = Language('Python', 'py', interpreter=self.ip)
        self.lp.id = 2
        
    
    def test_run_c(self):
        '''Test runner with a C submission'''
        
        self.sc = Submission(self.a ,self.lc, self.s)
        self.sc.source = r'''
#include <stdio.h>

int main(void) {
    printf("Hello World!\n");
    return 0;
}
'''
        self.sc.id = 1
        
        with Runner(self.sc) as r:
            compilation = r.compile()
            self.assertTrue(compilation, 'C compilation failed')
            self.assertEqual(compilation.returncode, 0, 'C compilation failed')
            if not compilation or compilation.returncode == 0:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertTrue(testrun, 'C testrun failed')
    
    def test_run_python(self):
        '''Test runner with a python submission'''

        self.sp = Submission(self.a, self.lp, self.s)
        self.sp.source = r'''
print "Hello World!"
'''
        self.sp.id = 2
        
        with Runner(self.sp) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Python compilation failed')
            if not compilation or compilation.returncode == 0:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertTrue(testrun, 'Python testrun failed')
    
    def test_run_fail(self):
        '''Test runner with a incorrect output'''
        
        self.sf = Submission(self.a, self.lp, self.s)
        self.sf.source = r'''
print "Hello!"
'''
        self.sf.id = 3
        
        with Runner(self.sf) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Wrong compilation failed')
            if not compilation or compilation.returncode == 0:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertFalse(testrun, 'Wrong testrun failed')
    
    def test_run_timeout(self):
        '''Test runner with an always reached timeout value'''
        
        self.st = Submission(self.a, self.lp, self.s)
        self.st.source = r'''
import time
time.sleep(2)
print "Hello World!"
'''
        self.st.id = 4
        
        with Runner(self.st) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Timeout compilation failed')
            if not compilation or compilation.returncode == 0:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertFalse(testrun, 'Timeout testrun failed')
