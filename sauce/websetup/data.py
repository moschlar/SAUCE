# -*- coding: utf-8 -*-
'''
Created on 17.03.2012

@author: moschlar
'''

import logging
from datetime import datetime, timedelta
from tg import config
from sauce import model
from sauce.model import DBSession as Session, Assignment, Test, Student, Language, Compiler, Interpreter, Submission, Contest, User
import transaction
import os

log = logging.getLogger(__name__)

def dummy_data(command, conf, vars):
    #log.debug(command)
    #log.debug(conf)
    #log.debug(vars)
    
    log.info('Inserting dummy data...')
    
    c = Contest(name='Contest Pi', description='This is a contest about programing. Hah! Who would have guessed that...',
                start_time=datetime.now(), end_time=datetime.now()+timedelta(days=1))
    Session.add(c)
    
    cd = Contest(name='Contest Omega', description='This is a contest is all over. <br /> But is has some <strong>HTML</strong> in it!',
                start_time=datetime.now()-timedelta(weeks=1), end_time=datetime.now()-timedelta(days=1))
    Session.add(cd)
    
    # C compiler
    cc = Compiler(name='GCC', path='/usr/bin/gcc', 
                  argv='-Wall {srcfile} -o {binfile}', timeout=5)
    Session.add(cc)
    
    # C language
    lc = Language(name='C', extension_src='c', compiler=cc)
    Session.add(lc)
    
    # Java compiler
    cj = Compiler(name='JDK', path='/usr/bin/javac',
                  argv='{srcfile}', timeout=10)
    Session.add(cj)
    
    # Java interpreter
    ij = Interpreter(name='JDK', path='/usr/bin/java',
                     argv='-cp {path} {basename}')
    Session.add(ij)
    
    # Java language
    lj = Language(name='Java 7', extension_src='java', 
                  extension_bin='class', compiler=cj, interpreter=ij)
    Session.add(lj)
    
    # Python interpreter
    ip = Interpreter(name='Python 2.7', path='/usr/bin/python2.7', 
                     argv='{binfile}')
    Session.add(ip)
    
    # Python language
    lp = Language(name='Python', extension_src='py', 
                  extension_bin='py', interpreter=ip)
    Session.add(lp)
    
    # Assignment
    a1 = Assignment(name='First Assignment', 
                    description='Write a program that says "Hello World!"', 
                    timeout=1, allowed_languages=[lc, lp, lj], 
                    show_compiler_msg=True, event=c)
    Session.add(a1)
    
    # Test
    t1 = Test(type='stdin_stdout', assignment=a1, visible=True, 
              output='Hello World!')
    Session.add(t1)
    
    a2 = Assignment(name='Square it!',
                    description='Write a program that calculates the powers of two for a given sequence of numbers. ' + 
                    'The numbers will consist only of integer values. The input shall be read from standard input and ' + 
                    'the output shall be written to standard output.',
                    timeout=2, allowed_languages=[lc, lp, lj],
                    show_compiler_msg=True, event=c)
    Session.add(a2)
    
    # Tests
    t2 = Test(type='stdin_stdout', assignment=a2, visible=True)
    t2.input = '''
1
2
3
4
5
'''
    t2.output = '''
1
4
9
16
25
'''
    Session.add(t2)
    
    t3 = Test(type='stdin_stdout', assignment=a2, visible=False)
    t3.input = '''
-5
-4
-3
-2
-1
0
'''
    t3.output = '''
25
16
9
4
1
0
'''
    Session.add(t3)
    
    # Students
    u1 = User(user_name=u'student', email_address=u'stu@dent.de', 
              display_name=u'Stu Dent')
    u1.password = u'studentpass'
    Session.add(u1)
    s1 = Student(name=u'Stu Dent', user=u1)
    Session.add(s1)
    
    u2 = User(user_name=u'student2', email_address=u'student@de.de', 
         display_name=u'Hänschen Klein')
    u2.password = u'studentpass'
    Session.add(u2)
    s2 = Student(name=u'Hänschen Klein', user=u2)
    Session.add(s2)
    
    transaction.commit()
    
    # A Submission in C
    sc = Submission(assignment=a1 ,language=lc, student=s1)
    sc.source = r'''
#include <stdio.h>

int main(void) {
    printf("Hello World!\n");
    return 0;
}
'''
    Session.add(sc)
    
    transaction.commit()
    
    # A Submission in Python
    sp = Submission(assignment=a1, language=lp, student=s1)
    sp.source = r'''
print "Hello World!"
'''
    Session.add(sp)
    
    transaction.commit()
    
    # A timing out Submission
    st = Submission(assignment=a1, language=lp, student=s2)
    st.source = r'''
import time
time.sleep(2)
print "Hello World!"
'''
    Session.add(st)
    
    sub = Submission(assignment=a2, language=lp, student=s2)
    sub.source = r'''
import sys
for line in sys.stdin:
    print int(line)**2
'''
    Session.add(sub)
    
    sf = Submission(assignment=a2, language=lp, student=s1)
    sf.source = r'''
print 1
print 4
print 9
print 16
print 25
'''
    Session.add(sf)
    
    a3 = Assignment(name='Zerotuples',
                    description='Find tuples of numbers in an unsorted input list ' +
                    'that sum up to zero <br />' + 
                    'Your program has to put out the positive part of the tuple ' + 
                    'in ascending order.',
                    timeout=10.0, allowed_languages=[lc, lp, lj],
                    show_compiler_msg=True, event=c)
    Session.add(a3)
    
    t3z = Test(type='stdin_stdout', assignment=a3, visible=True, timeout=2.0)
    t3z.input = r'''
0.5
-1.0
3.1415
1.0
-0.5
'''
    t3z.output = r'''
0.5
1.0
'''
    Session.add(t3z)
    
    t10 = Test(type='stdin_stdout', assignment=a3, visible=False, timeout=20.0)
    t10.input = open(os.path.join(os.path.dirname(__file__), 'data', 'question')).read()
    t10.output = open(os.path.join(os.path.dirname(__file__), 'data', 'answer')).read()
    Session.add(t10)
    
    s10 = Submission(assignment=a3, language=lp, student=s2)
    s10.source = open(os.path.join(os.path.dirname(__file__), 'data', 'answer.py')).read()
    
    s11 = Submission(assignment=a3, language=lp, student=s2)
    s11.source = open(os.path.join(os.path.dirname(__file__), 'data', 'answer2.py')).read()
    
    Session.add_all([s10, s11])
    
    transaction.commit()
    
    log.info('Dummy data inserted.')
