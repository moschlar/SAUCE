'''
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
        
        self.a = Assignment(id=1, name='Assignment A', 
                            description='Write a program that says "Hello World!"', 
                            timeout=1)
        
        self.t = Test(type='stdin_stdout', assignment=self.a, 
                      output='Hello World!')
        
        self.s = Student(name='Stu Dent')
        
        self.cc = Compiler(id=1, name='GCC', path='/usr/bin/gcc', 
                           argv='{srcfile} -o {objfile}', timeout=5)
        
        self.lc = Language(id=1, name='C', extension_src='c', 
                           compiler=self.cc)
        
        
        self.ip = Interpreter(id=1, name='Python 2.7', 
                              path='/usr/bin/python2.7', argv='{binfile}')
        
        self.lp = Language(id=2, name='Python', extension_src='py', 
                           extension_bin='py', interpreter=self.ip)
        
    
    def test_run_c(self):
        '''Test runner with a C submission'''
        
        self.sc = Submission(id=1, assignment=self.a, 
                             language=self.lc, student=self.s)
        self.sc.source = r'''
#include <stdio.h>

int main(void) {
    printf("Hello World!\n");
    return 0;
}
'''
        
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

        self.sp = Submission(id=2, assignment=self.a, 
                             language=self.lp, student=self.s)
        self.sp.source = r'''
print "Hello World!"
'''
        
        with Runner(self.sp) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Python compilation failed')
            if not compilation or compilation.returncode == 0:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertTrue(testrun, 'Python testrun failed')
    
    def test_run_fail(self):
        '''Test runner with a incorrect output'''
        
        self.sf = Submission(id=3, assignment=self.a, 
                             language=self.lp, student=self.s)
        self.sf.source = r'''
print "Hello!"
'''
        
        with Runner(self.sf) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Wrong compilation failed')
            if not compilation or compilation.returncode == 0:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertFalse(testrun, 'Wrong testrun failed')
    
    def test_run_timeout(self):
        '''Test runner with an always reached timeout value'''
        
        self.st = Submission(id=4, assignment=self.a, 
                             language=self.lp, student=self.s)
        self.st.source = r'''
import time
time.sleep(2)
print "Hello World!"
'''
        
        with Runner(self.st) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Timeout compilation failed')
            if not compilation or compilation.returncode == 0:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertFalse(testrun, 'Timeout testrun failed')
