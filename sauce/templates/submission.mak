<%inherit file="local:templates.master"/>

<%def name="title()">
  Submission
</%def>

<h2>Submission ${submission.id}</h2>

<h3>For Assignment: ${h.html.tags.link_to(submission.assignment.name, tg.url('/assignments/%d' % submission.assignment.id))}</h3>

<table>
  <tr><th>Language:</th><td>${submission.language}</td></tr>
  <tr><th>Compiler:</th><td>${submission.language.compiler}</td></tr>
  <tr><th>Interpreter:</th><td>${submission.language.interpreter}</td></tr>
</table>

<p>Submitted at: ${submission.date}</p>

<h4>Source code:</h4>
<pre class="code">${submission.source}</pre>

<h4>Test runs:</h4>
% if submission.testruns:
  <ul>
  % for testrun in reversed(submission.testruns):
    <li>${testrun.date} - ${testrun.result}</li>
  % endfor
% else:
  <p>No test has been run so far. <br />
  ${h.link_for('Request test run', tg.url('/submissions/%d/test' % submission.id))}</p>
% endif
