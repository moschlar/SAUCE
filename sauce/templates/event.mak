<%inherit file="local:templates.master"/>

<%
from datetime import datetime
%>

<%def name="title()">
  Event
</%def>

##<h2>Event "${event.name}"</h2>

<h2>${event.name}</h2>

<p>${event.description}</p>

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
  <p>Remaining time: ${event.remaining_time}</p>
% else:
  <p>Event is finished</p>
%endif

% if event.assignments:
  <h4>Assignments</h4>
   <table>
    %for assignment in event.assignments:
    <tr>
      <th>${h.html.tags.link_to(assignment.name, tg.url('/assignments/%d' % assignment.id))}</th>
      <td>${assignment.description}</td>
    </tr>
    %endfor
    </table>
% endif