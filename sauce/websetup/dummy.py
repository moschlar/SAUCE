# -*- coding: utf-8 -*-
'''
Created on 07.04.2012

@author: moschlar
'''

import logging
from datetime import datetime, timedelta
from tg import config
from sauce import model
from sauce.model import (DBSession as Session, Assignment, Test, Sheet, User,
                         Language, Compiler, Interpreter, Submission, Lesson,
                         Course, Contest, Team, Testrun, Judgement)
import transaction
from random import choice

log = logging.getLogger(__name__)


def course_data(command, conf, vars):
    # Dirty hack
    # If we are in testing mode, we don't want the tests to be ran
    if 'mode' in conf and conf['mode'] == 'test':
        choose = lambda x: False
    else:
        choose = choice

    # C compiler
    cc = Compiler(name=u'GCC', path=u'/usr/bin/gcc',
                  argv=u'-Wall {srcfile} -o {binfile}', timeout=5)
    Session.add(cc)

    # C language
    lc = Language(name=u'C', extension_src=u'c', compiler=cc, lexer_name=u'cpp')
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
    lj = Language(name=u'Java', extension_src=u'java', extension_bin=u'class',
                  compiler=cj, interpreter=ij, lexer_name=u'java')
    Session.add(lj)

    # Python interpreter
    ip = Interpreter(name=u'Python 2.7', path=u'/usr/bin/python2.7',
                     argv=u'{binfile}')
    Session.add(ip)

    # Python language
    lp = Language(name=u'Python', extension_src=u'py',
                  extension_bin=u'py', interpreter=ip, lexer_name=u'python')
    Session.add(lp)

    # Bash shell
    Session.add(Language(name=u'Bash',
        extension_src=u'sh',
        extension_bin=u'sh',
        lexer_name=u'bash',
        interpreter=Interpreter(name=u'Bash',
            path=u'/bin/bash',
            argv=u'{binfile}'))
        )

    teacher_master = User(user_name=u'teacher',
        display_name=u'Prof. Teacher', email_address=u'teacher@inf.de',
        password=u'teachpass')
    tutor = User(user_name=u'tutor',
        display_name=u'Dr. Tutor', email_address=u'tutor@inf.de',
        password=u'tutorpass')
    Session.add_all([teacher_master, tutor])

    course = Course(name=u'Programming 101 - Demo',
        description=u'<p>Lectured by Prof. Demo</p>',
        start_time=datetime.now(), end_time=datetime.now() + timedelta(days=31),
        password=u'', teacher=teacher_master,
        public=True, _url='demo')
    Session.add(course)

    lesson_a = Lesson(name=u'Lesson 1', event=course,
        tutor=tutor, lesson_id=1)
    Session.add(lesson_a)

    team_a = Team(name=u'Team A', lesson=lesson_a)
    team_b = Team(name=u'Team B', lesson=lesson_a)
    Session.add_all([team_a, team_b])

    stud_a1 = User(user_name=u'studenta1',
        display_name=u'Student A1', email_address=u'studenta1@inf.de',
        password=u'studentpass', teams=[team_a])
    stud_a2 = User(user_name=u'studenta2',
        display_name=u'Student A2', email_address=u'studenta2@inf.de',
        password=u'studentpass', teams=[team_a])
    stud_b1 = User(user_name=u'studentb1',
        display_name=u'Student B1', email_address=u'studentb1@inf.de',
        password=u'studentpass', teams=[team_b])
    Session.add_all([stud_a1, stud_a2, stud_b1])

    # First Sheet

    sh_1 = Sheet(name=u'Sheet 1', description=u'<p>Warmup.</p>',
        event=course, _teacher=teacher_master, sheet_id=1, public=True)
    Session.add(sh_1)

    ass_1 = Assignment(name=u'Hello Word',
        description=u'<p>Write a program that says Hello to Microsoft Word.</p>',
        public=True, sheet=sh_1, timeout=1.0, allowed_languages=[lj],
        show_compiler_msg=True, assignment_id=1)
    Session.add(ass_1)

    test_1 = Test(output_type=u'stdout', visible=True,
        output_data=u'Hello, Word?!', ignore_case=False,
        assignment=ass_1, user=teacher_master)
    Session.add(test_1)

    # Generate a random number of submissions
    for i in xrange(choice(xrange(3)) + 1):
        subm = Submission(user=stud_a1,
            language=lj, assignment=ass_1, filename=u'Hello.java',
            source=u'class Hello {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Hello, Word?!");\n\t}\n}\n')
        Session.add(subm)
        Session.flush()
        # Maybe run the tests
        if choose((True, False)):
            subm.run_tests()

    subm_2 = Submission(user=stud_a2, language=lj,
        assignment=ass_1, filename=u'Hello.java',
        source=u'class Hello {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Hello, Word?!");\n\t}\n}\n',
        testruns=[Testrun(test=test_1, output_data=u'Hello, Word?!',
            runtime=0.4711, result=True)])
    Session.add(subm_2)

    j_1 = Judgement(submission=subm_2, tutor=tutor,
                    annotations={4: 'Although your function is of return type void, you should return at the desired end of your function.'},
                    corrected_source=u'class Hello {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Hello Word?!");\n\t\treturn;\n\t}\n}\n')
    Session.add(j_1)

    # Second Sheet

    sh_2 = Sheet(name=u'Second Sheet', description=u'<p>And now for something completely different.</p><p>Some real exercises for semi-real-world problems. Like squaring numbers \'n stuff.</p>',
                 event=course, _teacher=teacher_master, sheet_id=2, public=True,
                 _start_time=datetime.now() + timedelta(days=2))
    Session.add(sh_2)

    ass_2 = Assignment(name=u'Square it!', description=u'Write a program that calculates the powers of two for a given sequence of numbers. ' +
                       u'The numbers will consist only of integer values. The input shall be read from standard input and ' +
                       u'the output shall be written to standard output.', public=True,
                       sheet=sh_2, timeout=1.0, allowed_languages=Language.query.all(),
                       show_compiler_msg=True, assignment_id=1,
                       _start_time=datetime.now(), _end_time=datetime.now() + timedelta(days=1))
    Session.add(ass_2)

    t2 = Test(input_type=u'stdin', output_type=u'stdout', assignment=ass_2,
        visible=True, user=teacher_master, splitlines=True, parse_int=True)
    t2.input_data = u'''
1
2
3
4
5
'''
    t2.output_data = u'''
1
4
9
16
25
'''
    Session.add(t2)

    t3 = Test(input_type=u'stdin', output_type=u'stdout', assignment=ass_2,
        visible=False, user=teacher_master, splitlines=True, parse_int=True)
    t3.input_data = u'''
-5
-4
-3
-2
-1
0
'''
    t3.output_data = u'''
25
16
9
4
1
0
'''
    Session.add(t3)

    lesson_b = Lesson(name=u'Second Lesson', event=course,
        tutor=teacher_master, lesson_id=2)
    Session.add(lesson_b)

    team_c = Team(name=u'Team C', lesson=lesson_b)
    Session.add(team_c)

    stud_c1 = User(user_name=u'studentc1', display_name=u'Student C1',
        email_address=u'studentc1@inf.de', password=u'studentpass',
        teams=[team_c])
    stud_c2 = User(user_name=u'studentc2', display_name=u'Student C2',
        email_address=u'studentc2@inf.de', password=u'studentpass',
        teams=[team_c])
    stud_c3 = User(user_name=u'studentc3', display_name=u'Student C3',
        email_address=u'studentc3@inf.de', password=u'studentpass',
        teams=[team_c])
    stud_d1 = User(user_name=u'studentd1', display_name=u'Student D1',
        email_address=u'studentd1@inf.de', password=u'studentpass',
        _lessons=[lesson_b])
    stud_d2 = User(user_name=u'studentd2', display_name=u'Student D2',
        email_address=u'studentd2@inf.de', password=u'studentpass',
        _lessons=[lesson_b])
    Session.add_all([stud_c1, stud_c2, stud_c3, stud_d1, stud_d2])

    source_variants = (u'class Hello {\n\tpublic static void main(String[] args) {\n\t\tSystem.out.println("Hello, Word?!");\n\t}\n}\n',
        u'''public class Hello
{
    public static void main(String[] args)
    {
        System.out.println("Hello, Word?!");
        return;
    }
}''',
u'''class Hello
{
    public static void main(String[] args)
    {
        System.out.println("Hello" + ", " + "Word?!");
    }
}''',
u'''public class Hello {
    public static void main(String[] args) {
        System.out.print("Hello, ");
        System.out.print("Word?!\\n");
        return;
    }
}''',
u'''class Hello
{
    public static void main(String[] args)
    {
        String s = new String("Hello, Word?!");
        System.out.println(s);
        return;
    }
}
''',
u'''public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World?!");
    }
}''')

    for stud in [stud_c1, stud_c2, stud_c3, stud_d1, stud_d2]:
        # Generate a random number of submissions
        for i in xrange(choice(xrange(3)) + 1):
            subm = Submission(user=stud,
                            language=lj, assignment=ass_1, filename=u'Hello.java',
                            # with a random source code variant
                            source=choice(source_variants))
            Session.add(subm)
            Session.flush()
            # Maybe run the tests
            if choose((True, False)):
                subm.run_tests()

    # WARNING: Changing the start parameter needs to be reflected in test_site
    for i, stud in enumerate((stud_a1, stud_a2, stud_c1), start=25):
        Session.add(Submission(id=i, user=stud, language=lj, assignment=ass_2,
            filename=u'Square.java', source=u'nothing to see here...'))
    Session.flush()

    transaction.commit()
