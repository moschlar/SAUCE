<%inherit file="local:templates.master"/>

<%! 
from datetime import datetime
%>

<%def name="title()">
  ${assignment.name} - Assignment
</%def>

<h2>${assignment.name}</h2>

<p class="description">${assignment.description | n }</p>

% if request.student:
  % if submissions:
    <h3>Your Submissions</h3>
    <ul>
    % for submission in reversed(submissions):
      <li>${h.html.tags.link_to(submission, tg.url('/submissions/%d' % submission.id))}
      % if submission.complete and submission.testrun:
        % if submission.testrun.result:
          <span class="green">(ok)</span>
        % else:
          <span class="red">(failed)</span>
        % endif
      % endif
      </li>
    % endfor
    </ul>
  % endif
  % if assignment.start_time < datetime.now() and assignment.end_time > datetime.now():
    <p>${h.html.tags.link_to('Submit new solution', tg.url('/assignments/%d/submit' % assignment.id))}</p>
  % else:
    <p>Submissions are already closed</p>
  % endif
% endif

% if assignment.visible_tests:
  <h3>Tests</h3>
  % if assignment.visible_tests:
    <table>
      <tr>
        <th>Input</th>
        <th>Output</th>
      </tr>
	  % for test in assignment.visible_tests:
	    <tr>
	      <td><pre class="code">${test.input}</pre></td>
	      <td><pre class="code">${test.output}</pre></td>
	    </tr>
	  % endfor
  </table>
  % endif
% endif

