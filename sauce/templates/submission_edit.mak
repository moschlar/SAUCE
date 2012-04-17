<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists" />

<%!
from difflib import unified_diff
%>

% if event:
<%def name="body_class()">class="navbar_left"</%def>
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
  % if compilation.result:
    <p class="green">Success</p>
  % else:
    <p class="red">Fail</p>
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
  ${lists.testruns(testruns)}
% endif


