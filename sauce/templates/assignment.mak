<%inherit file="local:templates.master"/>
<%namespace file="local:templates.misc" import="times_dl" />

<%def name="title()">
  ${assignment.name}
</%def>

<div class="page-header">
  <h1>${assignment.name} <small>Assignment</small></h1>
</div>

${self.details(assignment)}

<%def name="details(assignment)">

<p class="description">${assignment.description | n }</p>

${times_dl(assignment)}

##% if request.student:
  % if submissions:
    <h2>Your Submissions <span class="badge">${len(submissions)}</span></h2>
    <ul>
    % for submission in reversed(submissions):
      <li>${submission.link}
      % if submission.user != request.user:
        <i>(${submission.user.display_name})</i>
      % endif
      % if submission.complete:
        % if submission.result:
          <span class="label label-success">ok</span>
        % else:
          <span class="label label-important">failed</span>
        % endif
      % else:
        <span class="label">n/a</span>
      % endif
      </li>
    % endfor
    </ul>
  % endif
  
  % if request.teacher or request.student and assignment.is_active:
    <p><a href="${tg.url('%s/submit' % (assignment.url))}" class="btn btn-primary">Submit new solution</a></p>
##  % else:
##    <p>Submissions are already closed.</p>
  % endif
##% endif

% if assignment.timeout:
  <p>General timeout: ${assignment.timeout} seconds</p>
% endif
% if assignment.visible_tests:
  <h2>Tests</h2>
    <table>
      <tr>
        <th>Input</th>
        <th>Output</th>
      </tr>
    % for test in assignment.visible_tests:
      <tr>
        <td><pre>${test.input_data}</pre></td>
        <td><pre>${test.output_data}</pre></td>
      </tr>
    % endfor
  </table>
% endif

</%def>

