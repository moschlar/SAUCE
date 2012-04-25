<%inherit file="local:templates.master"/>

<%def name="title()">
  About
</%def>

<h2>SAUCE</h2>
<h3>About</h3>

<p>
SAUCE is a web-based system for automated testing of 
programming exercises.
It aims to help both students and teachers by providing
an environment for correcting, testing and annotating
source code.</p>

<p>SAUCE is developed as the practical part of a bachelor 
thesis in computer science by Moritz Schlarb.</p>

<p>SAUCE uses some state-of-the-art technologies for rapid web
development like the
<a href="http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller">Model-View-Controller pattern</a>
using a sophisticated framework (<a href="http://turbogears.org/">TurboGears2</a>),
an <a href="http://en.wikipedia.org/wiki/Object-relational_mapping">object
relational mapper</a> (<a href="http://www.sqlalchemy.org/">SQLAlchemy</a>),
both written in the most flexible and beautiful programming language,
<a href="http://www.python.org/">Python</a>.<br />
We use <a href="http://git-scm.com/">Git</a> for soure code management and
<a href="https://github.com/">Github</a> as an open source project hosting
platform.</p>

<h3>How it works</h3>

<h4>Main entities</h4>
<p>
There are two groups of user accounts: Students and Teachers.
A Student belongs to a Team which belongs to a Lesson which belongs
to an Event. A Lesson is taught by a Teacher. An Event has a Teacher
who is responsible for creating Sheets, Assignments and Tests.<br />
A Student may submit Submissions for any Assignment that belongs to an
Event he is enrolled in that is currently active.<br />
A Teacher is can view all Submissions made by Students in his Lessons
and create Judgements for them.
</p>

<p>
When a Submission is submitted by a Student, it gets automatically
tested with the Test cases that were defined for that Assignment.
Test cases can be visible for the Student or hidden.
The Student gets immediate feedback if his program did solve the 
visible Test case correctly or not. He may only continue submitting,
when the visible Test cases are correctly solved.<br />
The Student may not submit when he fails solving the visible Test case,
but his Submission is saved in the database anyway, so it is up to the
lesson's teacher to judge whether his solution is partially correct or
not.<br />
In general, the automatic judgement does not aim to replace the human
judgement provided by Teachers. It's only goal is to simplify the
validation and judgement processes by providing a contemporary
framework.
</p>