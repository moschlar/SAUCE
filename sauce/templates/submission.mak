<%inherit file="local:templates.master"/>

<%def name="title()">
  Submission
</%def>

<h2>Submission</h2>

<div>
% if assignmenta and hasattr(assignment, 'id'):
Assignment: ${assignment.id}
% endif
<br />
% if submission and hasattr(submission, 'id'):
Submission: ${submission.id}
% endif
</div>

##<h3>Submission for Assignment: 
##${h.html.tags.link_to(assignment.name, tg.url('/assignments/%d' % assignment.id))}</h3>

% if not submission.complete:
  ${c.form(c.options, child_args=c.child_args) | n}
% endif

% if compilation:
  <h3>Compilation result</h3>
  % if compilation.returncode == 0:
  <p>Success</p>
  % else:
  <p>Fail</p>
  % endif
  <table>
  <tr><th>stdout</th><th>stderr</th></tr>
  <tr><td><pre>${compilation.stdout}</pre></td><td><pre>${compilation.stderr}</pre></td></tr>
  </table>
% endif

% if testruns:
  <h3>Testrun results</h3>
  % for testrun in testruns:
  % if testrun.result:
  <p>Success</p>
  % else:
  <p>Fail</p>
  % endif
  <table>
  <tr><th>Given input</th><th>Expected stdout</th><th>Real stdout</th><th>Real stderr</th></tr>
  <tr><td><pre>${testrun.test.input}</pre></td><td><pre>${testrun.test.output}</pre></td><td><pre>${testrun.process.stdout}</pre></td>
  <td><pre>${testrun.process.stderr}</pre></td></tr>
  </table>
  % endfor
% endif
  