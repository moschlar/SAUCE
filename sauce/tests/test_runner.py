# -*- coding: utf-8 -*-
'''
@since: 15.03.2012

@author: moschlar
'''
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase
from sauce.tests import *

from sauce.model import Assignment, Submission, Language, Compiler, Interpreter, Test, User

from sauce.lib.runner import Runner, MAX_DATA_LENGTH

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

        self.aa = Assignment(
            id=2, name='Assignment B',
            description='Write a program that says Hello to someone from a file to a file.',
            timeout=1)

        self.tt = Test(input_type='file', output_type='file',
            assignment=self.aa, input_data='World', output_data='Hello World!',
            argv='{infile} {outfile}')

        self.s = User(user_name='student', display_name='Stu Dent',
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
                    self.assertTrue(testrun.result, 'C testrun failed')

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
                    self.assertTrue(testrun.result, 'Python testrun failed')

    def test_run_python_file(self):
        '''Test runner with a python submission and file input/output'''

        self.sp = Submission(id=7, assignment=self.aa,
                             language=self.lp, user=self.s)
        self.sp.source = r'''
import sys
filein = sys.argv[1]
fileout = sys.argv[2]
with open(filein, 'r') as fi:
    with open(fileout, 'w') as fo:
        fo.write("Hello %s!" % fi.read())
'''

        with Runner(self.sp) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Python compilation failed')
            if not compilation or compilation.result:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertTrue(testrun.result, 'Python testrun failed')

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
                    self.assertTrue(testrun.result, 'Java testrun failed')

    def test_compile_fail(self):
        '''Test runner with non-compiling java submission'''

        self.sj = Submission(id=6, assignment=self.a,
                             language=self.lj, user=self.s)
        self.sj.source = r'''
public class World {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}
'''
        self.sj.filename = 'Hello.java'

        with Runner(self.sj) as r:
            compilation = r.compile()
            self.assertTrue(compilation, 'Java compilation failed')
            self.assertFalse(compilation.result, 'Java compilation should fail')

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
                    print testrun
                    self.assertFalse(testrun.result, 'Wrong testrun failed')

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
                    self.assertFalse(testrun.result, 'Timeout testrun failed')

    def test_run_max_length(self):
        '''Test runner with too much output'''

        self.st = Submission(id=8, assignment=self.a,
                             language=self.lp, user=self.s)
        self.st.source = r'''
import sys
print 'x' * (%d + 1024)
print >>sys.stderr, 'y' * (%d + 1024)
''' % (MAX_DATA_LENGTH, MAX_DATA_LENGTH)

        print self.st.source

        with Runner(self.st) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'max_length compilation failed')
            if not compilation or compilation.result:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertFalse(testrun.result, 'max_length testrun failed')
                    self.assertIn('TRUNCATED', testrun.output_data)
                    self.assertIn('TRUNCATED', testrun.error_data)

    def test_run_timeout_evil(self):
        '''Test runner with a process that ignores SIGTERM'''

        self.st = Submission(id=10, assignment=self.a,
                             language=self.lp, user=self.s)
        self.st.source = r'''
import time
import signal
signal.signal(signal.SIGTERM, signal.SIG_IGN)
print "Hello World!"
time.sleep(2)
'''

        with Runner(self.st) as r:
            compilation = r.compile()
            self.assertFalse(compilation, 'Evil timeout compilation failed')
            if not compilation or compilation.result:
                testruns = [testrun for testrun in r.test()]
                for testrun in testruns:
                    self.assertFalse(testrun.result, 'Evil timeout testrun failed')
