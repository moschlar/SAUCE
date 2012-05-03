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
  % if compilation.stdout or compilation.stderr:
    <table style="border: 1px solid black; width:690px; max-width: 690px;">
    % if compilation.stdout:
      <tr>
        <th>stdout</th>
        <td><pre class="code">${compilation.stdout}</pre></td>
      </tr>
    % endif
    % if compilation.stderr:
      <tr>
        <th>stderr</th>
        <td><pre class="code">${compilation.stderr}</pre></td>
      </tr>
    % endif
    </table>
  % endif
% endif

% if testruns:
  ${lists.testruns(testruns)}
% endif


