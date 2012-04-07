<%inherit file="local:templates.master"/>

<%!
from difflib import unified_diff
%>

% if event:
<%def name="body_class()">navbar_left</%def>
% endif


<%def name="title()">
  Submission
</%def>

${' &gt '.join(breadcrumbs) | n}

<h2>Submission 
% if submission and hasattr(submission, 'id'):
  ${submission.id}
% endif
</h2>

<p>
% if submission.assignment:
for Assignment: ${submission.assignment.link}
% endif
</p>

${c.form(c.options, child_args=c.child_args) | n}

% if compilation:
  <h3>Compilation result</h3>
  % if compilation.returncode == 0:
    <p>Success</p>
  % else:
    <p>Fail</p>
  % endif
  <table>
  <tr>
    <th>stdout</th><th>stderr</th>
  </tr>
  <tr>
    <td><pre>${compilation.stdout}</pre></td>
    <td><pre>${compilation.stderr}</pre></td>
  </tr>
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
      <tr>
        <th>Given input</th>
        <th>Expected stdout</th>
        <th>Real stdout</th>
        <th>Real stderr</th>
      </tr>
      <tr>
        <td><pre>${testrun.test.input_data}</pre></td>
        <td><pre>${testrun.test.output_data}</pre></td>
        <td><pre>${testrun.output_data}</pre></td>
        <td><pre>${testrun.error_data}</pre></td>
      </tr>
    </table>
  % endfor
% endif


