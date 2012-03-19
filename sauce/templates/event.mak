<%inherit file="local:templates.master"/>

<%def name="title()">
  Event
</%def>

<h2>Event</h2>

<h3>${event.name}</h3>

<p>${event.description}</p>

<p>Running from ${event.start_time } to ${event.end_time }</p>

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