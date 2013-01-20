<%inherit file="local:templates.master" />

<%def name="title()">
  About
</%def>


<div class="page-header">
  <h1>About</h1>
</div>

<div class="row"><div class="span9">

<p>
<strong>SAUCE</strong> is a web-based system for automated testing of 
programming exercises.
It aims to help both students and teachers by providing
an environment for correcting, testing and annotating
source code.</p>

<p><strong>SAUCE</strong> uses some state-of-the-art technologies for rapid web
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

<h3>See also</h3>
The <a href="${tg.url('/docs/')}">documentation page</a> holds several
pages of documentation about the usage and configuration of <strong>SAUCE</strong>.

<div>&nbsp;</div>

<div class="well">
  <h2>Acknowledgements</h2>
  <p>
    <strong>SAUCE</strong> wouldn't be possible without some other
    great open source projects and people. I'd like to thank all of
    them for their work, including but not limited to:
  </p>
  <dl>
    <dt><a href="http://turbogears.org/">TurboGears 2</a></dt>
    <dd>The Webframework</dd>
    <dt><a href="http://toscawidgets.org/">Toscawidgets 2</a></dt>
    <dd>The Widget library</dd>
    <dt><a href="http://www.sqlalchemy.org/">SQLAlchemy</a></dt>
    <dd>The Python SQL Toolkit and Object Relational Mapper</dd>
    <dt><a href="http://twitter.github.com/bootstrap">Twitter Bootstrap</a></dt>
    <dd>The CSS framework - which includes <a href="http://jquery.com/">jQuery</a>
      and <a href="http://glyphicons.com/">Glyphicons Free</a></dd>
    <dt><a href="http://pygments.org/">Pygments</a></dt>
    <dd>The Python Syntax Highlighter</dd>
  </dl>
  <p><small>And many more...</small></p>
</div>

</div></div>
