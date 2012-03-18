<%inherit file="local:templates.master"/>

<%def name="title()">
  Submission
</%def>

<h2>Submission</h2>

<h3>Submission for Assignment: ${h.html.tags.link_to(submission.assignment.name, tg.url('/assignments/%d' % submission.assignment.id))}</h3>

<p>Language: ${submission.language}, Compiler: ${submission.language.compiler}, Interpreter: ${submission.language.interpreter}</p>

<h4>Source code:</h4>
<pre>
${submission.source}
</pre>

<h4>Test runs:</h4>
% if submission.testruns:
  <ul>
  % for testrun in reversed(submission.testruns):
    <li>${testrun.date} - ${testrun.result}</li>
  % endfor
% else:
  <p>No test has been run so far. <br />
% endif
${h.link_for('Request test run', tg.url('/submissions/%d/test' % submission.id))}</p>
