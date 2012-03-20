<%inherit file="local:templates.master"/>

<%def name="title()">
  Submission
</%def>

<h2>Submission</h2>

<div>
% if assignment_id:
Assignment: ${assignment_id}
% endif
<br />
% if submission_id:
Submission: ${submission_id}
% endif
</div>

##<h3>Submission for Assignment: 
##${h.html.tags.link_to(assignment.name, tg.url('/assignments/%d' % assignment.id))}</h3>

${c.form(c.options, child_args=c.child_args) | n}

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
  