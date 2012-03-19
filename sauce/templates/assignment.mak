<%inherit file="local:templates.master"/>

<%! 
from datetime import datetime
%>

<%def name="title()">
  ${assignment.name} - Assignment
</%def>

<h2>${assignment.name}</h2>

<p class="description">${assignment.description}</p>

% if request.student:
  % if submissions:
    <h3>Your Submissions</h3>
    <ul>
    % for submission in reversed(submissions):
      <li>${h.html.tags.link_to(submission, tg.url('/submissions/%d' % submission.id))}</li>
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
  % for test in assignment.visible_tests:
    <h4>Input:</h4>
      <pre class="code">${test.input}</pre>
    <h4>Output:</h4>
      <pre class="code">${test.output}</pre>
  % endfor
% endif

