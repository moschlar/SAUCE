<%inherit file="local:templates.master"/>

<%
from datetime import datetime
%>

<%def name="title()">
 ${event.name} - Event
</%def>

<h2>${event.name}</h2>

<p class="description">${event.description}</p>

<table>
  <tr>
    <th>Start time:</th>
    <th>End time:</th>
  </tr>
  <tr>
    <td>${event.start_time }</td>
    <td>${event.end_time }</td>
  </tr>
</table>

% if event.is_active:
  <table><tr>
    <th>Remaining time:</th>
    <td>${event.remaining_time}</td>
  </tr></table>
% else:
  <p>Event is finished</p>
%endif

% if event.assignments:
  <h3>Assignments</h3>
  <dl>
    %for assignment in event.assignments:
      <dt>${h.html.tags.link_to(assignment.name, tg.url('/assignments/%d' % assignment.id))}</dt>
      <dd>${assignment.description}</dd>
    %endfor
  </dl>
% endif