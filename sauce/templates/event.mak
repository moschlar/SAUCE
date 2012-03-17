<%inherit file="local:templates.master"/>

<%def name="title()">
  Event
</%def>

<h2>Event</h2>

<h3>${event.name}</h3>

<p>${event.description}</p>

% if event.assignments:
  <h4>Assignments</h4>
    %for assignment in event.assignments:
    <tr>
      <td>${h.html.tags.link_to(assignment.title, tg.url('/assignments/%d' % assignment.id))}</td>
      <td>${assignment.description}</td>
    </tr>
    %endfor
% endif