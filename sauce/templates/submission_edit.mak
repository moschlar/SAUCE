<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists" />

<%def name="title()">
<%
  try:
    heading = 'Submission %d' % submission.id
  except:
    heading = 'Submission'
  %>
  ${heading}
</%def>

<div class="page-header">
  <h1>${self.title()}
    % if submission.assignment:
      <small>for Assignment: ${submission.assignment.link}</small>
    % endif
  </h1>
</div>

<p>Created: ${submission.created.strftime('%x %X')},
  Last modified: ${submission.modified.strftime('%x %X')}</p>

${c.form(c.options, child_args=c.child_args) | n}

% if compilation:
  <h3>Compilation result</h3>
  % if compilation.result:
    <p class="label label-success">Success</p>
  % else:
    <p class="label label-important">Fail</p>
  % endif
  % if compilation.stdout or compilation.stderr:
    <table style="border: 1px solid black; width:690px; max-width: 690px;">
    % if compilation.stdout:
      <tr>
        <th>stdout</th>
        <td><pre>${compilation.stdout}</pre></td>
      </tr>
    % endif
    % if compilation.stderr:
      <tr>
        <th>stderr</th>
        <td><pre>${compilation.stderr}</pre></td>
      </tr>
    % endif
    </table>
  % endif
% endif

% if testruns:
  ${lists.testruns(testruns)}
% endif


