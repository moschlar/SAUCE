<%inherit file="local:templates.master"/>

<%
from datetime import datetime

%>

<%def name="title()">
 ${event.name} - Event
</%def>

<h2>${event.name}</h2>

<p class="description">${event.description | n }</p>

<table>
  <tr>
    <th>Start time:</th>
    <th>End time:</th>
  </tr>
  <tr>
    <td>${event.start_time.strftime('%x %X')}</td>
    <td>${event.end_time.strftime('%x %X')}</td>
  </tr>
</table>

% if event.is_active:
  <table><tr>
    <th>Remaining time:</th>
    <td>${h.strftimedelta(event.remaining_time)}</td>
  </tr></table>
% else:
  <p>Event is finished.</p>
%endif

% if event.assignments:
  <h3>Assignments</h3>
  <dl>
    %for assignment in event.assignments:
      <dt>${h.link(assignment.name, tg.url('/assignments/%d' % assignment.id))}</dt>
      <dd>${assignment.description | n, h.striphtml }</dd>
    %endfor
  </dl>
% endif

% if event.news:
  <h3>News</h3>
  
  % for newsitem in event.news:
    <div style="font-weight: bold;">${newsitem.subject}</div>
    <div>${newsitem.message | n}</div>
  % endfor
% endif