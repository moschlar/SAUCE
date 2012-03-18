'''
Created on 17.03.2012

@author: moschlar
'''
import logging
from tg import config
from sauce import model
from sauce.model import DBSession as Session, Assignment, Test, Student, Language, Compiler, Interpreter, Submission, Contest
import transaction

log = logging.getLogger(__name__)

def dummy_data(command, conf, vars):
    log.debug(command)
    log.debug(conf)
    log.debug(vars)
    
    c = Contest(name='Contest Pi')
    Session.add(c)
    
    # C compiler
    cc = Compiler(name='GCC', path='/usr/bin/gcc', 
                  argv='{srcfile} -o {objfile}', timeout=5)
    Session.add(cc)
    
    # C language
    lc = Language(name='C', extension='c', compiler=cc)
    Session.add(lc)
    
    # Python interpreter
    ip = Interpreter(name='Python 2.7', path='/usr/bin/python2.7', 
                     argv='{srcfile}')
    Session.add(ip)
    
    # Python language
    lp = Language(name='Python', extension='py', interpreter=ip)
    Session.add(lp)
    
    # Assignment
    a1 = Assignment(name='First Assignment', 
                    description='Write a program that says "Hello World!"', 
                    timeout=1, allowed_languages=[lc, lp], 
                    show_compiler_msg=True, event=c)
    Session.add(a1)
    
    # Test
    t1 = Test(type='stdin_stdout', assignment=a1, visible=True, 
              output='Hello World!')
    Session.add(t1)
    
    # Student
    s1 = Student(name='Stu Dent')
    Session.add(s1)

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
    st = Submission(assignment=a1, language=lp, student=s1)
    st.source = r'''
import time
time.sleep(2)
print "Hello World!"
'''
    Session.add(st)
    
    transaction.commit()
