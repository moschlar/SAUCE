'''
Created on 15.03.2012

@author: moschlar
'''
from unittest import TestCase
from sauce.tests import *

from sauce.model import Assignment, Submission, Language, Compiler, Interpreter, Test, Student

from sauce.lib.runner import Runner

__all__ = ['TestRunner']


class TestRunner(TestCase):
    '''Perform simple "Hello World!" tests on the runner library'''
    
    def setUp(self):
        '''Set up test with a simple assignment and test case'''
        
        self.a = Assignment(id=1, name='Assignment A',
                            description='Write a program that says "Hello World!"',
                            timeout=1)
        
        self.t = Test(input_type='stdin', output_type='stdout',
            assignment=self.a, output_data='Hello World!')
        
        self.s = Student(user_name='student', display_name='Stu Dent',
            password='studentpass', email_address='stu@dent.de')
        
        self.cc = Compiler(id=1, name='GCC', path='/usr/bin/gcc', 
                           argv='{srcfile} -o {binfile}', timeout=5)
        
        self.lc = Language(id=1, name='C', extension_src='c', 
                           compiler=self.cc)
        
        
        self.ip = Interpreter(id=1, name='Python 2.7', 
                              path='/usr/bin/python2.7', argv='{binfile}')
        
        self.lp = Language(id=2, name='Python', extension_src='py', 
                           extension_bin='py', interpreter=self.ip)
    
        # Java compiler
        self.cj = Compiler(id=2, name='JDK', path='/usr/bin/javac',
                      argv='{srcfile}', timeout=10)
        
        # Java interpreter
        self.ij = Interpreter(id=2, name='JDK', path='/usr/bin/java',
                         argv='-cp {path} {basename}')
        
        # Java language
        self.lj = Language(id=3, name='Java', extension_src='java', 
                      extension_bin='class', compiler=self.cj, interpreter=self.ij)
    
    def test_run_c(self):
        '''Test runner with a C submission'''
        
        self.sc = Submission(id=1, assignment=self.a, 
                             language=self.lc, user=self.s)
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
            self.assertTrue(compilation.result, 'C compilation failed')
            if not compilation or compilation.result:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertTrue(testrun, 'C testrun failed')
    
    def test_run_python(self):
        '''Test runner with a python submission'''

        self.sp = Submission(id=2, assignment=self.a, 
                             language=self.lp, user=self.s)
        self.sp.source = r'''
print "Hello World!"
'''
        
        with Runner(self.sp) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Python compilation failed')
            if not compilation or compilation.result:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertTrue(testrun, 'Python testrun failed')
    
    def test_run_java(self):
        '''Test runner with java submission'''
        
        self.sj = Submission(id=5, assignment=self.a,
                             language=self.lj, user=self.s)
        self.sj.source = r'''
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}
'''
        self.sj.filename = 'Hello.java'
        
        with Runner(self.sj) as r:
            compilation = r.compile()
            self.assertTrue(compilation, 'Java compilation failed')
            self.assertTrue(compilation.result, 'Java compilation failed')
            if not compilation or compilation.result:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertTrue(testrun, 'Java testrun failed')
    
    def test_run_fail(self):
        '''Test runner with a incorrect output'''
        
        self.sf = Submission(id=3, assignment=self.a, 
                             language=self.lp, user=self.s)
        self.sf.source = r'''
print "Hello!"
'''
        
        with Runner(self.sf) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Wrong compilation failed')
            if not compilation or compilation.result:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertFalse(testrun, 'Wrong testrun failed')
    
    def test_run_timeout(self):
        '''Test runner with an always reached timeout value'''
        
        self.st = Submission(id=4, assignment=self.a, 
                             language=self.lp, user=self.s)
        self.st.source = r'''
import time
time.sleep(2)
print "Hello World!"
'''
        
        with Runner(self.st) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Timeout compilation failed')
            if not compilation or compilation.result:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertFalse(testrun, 'Timeout testrun failed')
