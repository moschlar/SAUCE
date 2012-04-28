<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists" />

<%def name="title()">
  Submission
</%def>

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

<p>Created: ${submission.created.strftime('%x %X')}, Last modified: ${submission.modified.strftime('%x %X')}</p>

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


