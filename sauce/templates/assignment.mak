<%inherit file="local:templates.master"/>
<%! 
from datetime import datetime
%>
<%def name="title()">
  Assignment
</%def>

<h2>SAUCE - Assignment</h2>

<h3>${assignment.name}</h3>

<p>${assignment.description}</p>

##<p><a href="${url(controller='assignment', action='submission', id=c.assignment.id)}">Submit solution</a></p>

% if request.student:
  % if assignment.start_time < datetime.now() and assignment.end_time > datetime.now():
    <p>${h.html.tags.link_to('Submit new solution', tg.url('/assignments/%d/submit' % assignment.id))}</p>
  % else:
    <p>Submissions are already closed</p>
  % endif
% endif

% if assignment.visible_tests:
  <h4>Tests:</h4>
  % for test in assignment.visible_tests:
    <h5>Input:</h5>
      <pre>${test.input}</pre>
    <h5>Output:</h5>
      <pre>${test.output}</pre>
  % endfor
% endif

