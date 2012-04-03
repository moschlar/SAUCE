# -*- coding: utf-8 -*-
'''
Created on 17.03.2012

@author: moschlar
'''

import logging
from datetime import datetime, timedelta
from tg import config
from sauce import model
from sauce.model import (DBSession as Session, Assignment, Test, Student, Sheet, 
                         Language, Compiler, Interpreter, Submission, Lesson, 
                         Course, Contest, Team, Teacher, Testrun, Judgement)
import transaction
import os

log = logging.getLogger(__name__)

def contest_data(command, conf, vars):
    
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
    s1 = Student(user_name=u'student', email_address=u'stu@dent.de', display_name=u'Stu Dent')
    s1.password = u'studentpass'
    Session.add(s1)
    
    s2 = Student(user_name=u'student2', email_address=u'student@de.de', display_name=u'Hänschen Klein')
    s2.password = u'studentpass'
    Session.add(s2)
    
    team = Team(name=u'Team Rocket', students=[s1, s2], events=[c])
    Session.add(team)
    
    #transaction.commit()
    
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
    
    #transaction.commit()
    
    # A Submission in Python
    sp = Submission(assignment=a1, language=lp, student=s1)
    sp.source = r'''
print "Hello World!"
'''
    Session.add(sp)
    
    #transaction.commit()
    
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
    
    t3z = Test(type='stdin_stdout', assignment=a3, visible=True)
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
    
    t10 = Test(type='stdin_stdout', assignment=a3, visible=False)
    t10.input = open(os.path.join(os.path.dirname(__file__), 'data', 'question')).read()
    t10.output = open(os.path.join(os.path.dirname(__file__), 'data', 'answer')).read()
    Session.add(t10)
    
    s10 = Submission(assignment=a3, language=lp, student=s2)
    s10.source = open(os.path.join(os.path.dirname(__file__), 'data', 'answer.py')).read()
    
    s11 = Submission(assignment=a3, language=lp, student=s2)
    s11.source = open(os.path.join(os.path.dirname(__file__), 'data', 'answer2.py')).read()
    
    Session.add_all([s10, s11])
    
    transaction.commit()
    

def course_data(command, conf, vars):
    
    # C compiler
    cc = Compiler(name=u'GCC', path=u'/usr/bin/gcc', 
                  argv=u'-Wall {srcfile} -o {binfile}', timeout=5)
    Session.add(cc)
    
    # C language
    lc = Language(name=u'C', extension_src=u'c', compiler=cc, brush=u'cpp')
    Session.add(lc)
    
    # Java compiler
    cj = Compiler(name=u'JDK', path=u'/usr/bin/javac',
                  argv=u'{srcfile}', timeout=10)
    Session.add(cj)
    
    # Java interpreter
    ij = Interpreter(name=u'JDK', path=u'/usr/bin/java',
                     argv=u'-cp {path} {basename}')
    Session.add(ij)
    
    # Java language
    lj = Language(name=u'Java 7', extension_src=u'java', extension_bin=u'class', 
                  compiler=cj, interpreter=ij, brush=u'java')
    Session.add(lj)
    
    # Python interpreter
    ip = Interpreter(name=u'Python 2.7', path=u'/usr/bin/python2.7', 
                     argv=u'{binfile}')
    Session.add(ip)
    
    # Python language
    lp = Language(name=u'Python', extension_src=u'py', 
                  extension_bin=u'py', interpreter=ip, brush=u'python')
    Session.add(lp)
    
    course = Course(name=u'EiP Sommersemester 2012', description=u'<p>Lectured by Prof. Dr. Elmar Schömer</p>',
               start_time = datetime.now(), end_time=datetime.now() + timedelta(days=7), password=u'PiE')
    Session.add(course)
    
    teacher_master = Teacher(user_name=u'teacher', display_name=u'Teacher Master', email_address=u'teacher@inf.de',
                             password=u'teachpass', events=[course])
    teacher_assistant = Teacher(user_name=u'teacherass', display_name=u'Teacher Assistant', email_address=u'teacherass@inf.de', 
                                password=u'teachpass', events=[course])
    Session.add_all([teacher_master, teacher_assistant])
    
    lesson = Lesson(name=u'Übungsgruppe 1', event=course, teacher=teacher_assistant)
    Session.add(lesson)
    
    team_a = Team(name=u'Team A', lesson=lesson)
    team_b = Team(name=u'Team B', lesson=lesson)
    Session.add_all([team_a, team_b])
    
    stud_a1 = Student(user_name=u'studenta1', display_name=u'Student A1', email_address=u'studenta1@inf.de',
                      password=u'studentpass', teams=[team_a])
    stud_a2 = Student(user_name=u'studenta2', display_name=u'Student A2', email_address=u'studenta2@inf.de',
                      password=u'studentpass', teams=[team_a])
    stud_b1 = Student(user_name=u'studentb1', display_name=u'Student B1', email_address=u'studentb1@inf.de',
                      password=u'studentpass', teams=[team_b])
    Session.add_all([stud_a1, stud_a2, stud_b1])
    
    sh_1 = Sheet(name=u'Übungsblatt 1', description=u'<p>Zum warmwerden.</p>',
                 event=course, teacher=teacher_master)
    
    ass_1 = Assignment(name=u'Hello Word', description=u'<p>Write a program that says Hello to Microsoft Word.</p>',
                       sheet=sh_1, timeout=1.0, allowed_languages=[lc, lj, lp], show_compiler_msg=True)
    Session.add(ass_1)
    
    test_1 = Test(output_type=u'stdout', visible=True, output_data=u'Hello, Word?!', 
                  assignment=ass_1, teacher=teacher_master)
    Session.add(test_1)
    
    subm_1 = Submission(student=stud_a1, language=lp, assignment=ass_1, filename=u'hello.py',
                        source=u'print "Hello, Word?!"')
    Session.add(subm_1)
    
    subm_2 = Submission(student=stud_a2, language=lj, assignment=ass_1, filename=u'Hello.java',
                        source=u'class Hello {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Hello Word?!");\n\t}\n}\n',
                        complete=True, testruns=[Testrun(test=test_1, output_data=u'Hello, Word?!', runtime=0.4711, result=True)])
    Session.add(subm_2)
    
    j_1 = Judgement(submission=subm_2, teacher=teacher_assistant, 
                    annotations={4: 'Although your function is of return type void, you should return at the desired end of your function.'})
    Session.add(j_1)
    
    transaction.commit()
