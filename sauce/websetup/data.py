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
    
    c = Contest('Contest Pi')
    Session.add(c)
    
    # C compiler
    cc = Compiler('GCC', '/usr/bin/gcc', '{srcfile} -o {objfile}', 5)
    Session.add(cc)
    
    # C language
    lc = Language('C', 'c', compiler=cc)
    Session.add(lc)
    
    # Python interpreter
    ip = Interpreter('Python 2.7', '/usr/bin/python2.7', '{srcfile}')
    Session.add(ip)
    
    # Python language
    lp = Language('Python', 'py', interpreter=ip)
    Session.add(lp)
    
    # Assignment
    a1 = Assignment('First Assignment', 'Write a program that says "Hello World!"', timeout=1, allowed_languages=[lc, lp], show_compiler_msg=True)
    a1.event = c
    Session.add(a1)
    
    # Test
    t1 = Test('stdin_stdout', a1, visible=True, output='Hello World!')
    Session.add(t1)
    
    # Student
    s1 = Student("Stu Dent")
    Session.add(s1)

    transaction.commit()
    
    # A Submission in C
    sc = Submission(a1 ,lc, s1)
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
    sp = Submission(a1, lp, s1)
    sp.source = r'''
print "Hello World!"
'''
    Session.add(sp)
    
    transaction.commit()
    
    # A timing out Submission
    st = Submission(a1, lp, s1)
    st.source = r'''
import time
time.sleep(2)
print "Hello World!"
'''
    Session.add(st)
    
    transaction.commit()