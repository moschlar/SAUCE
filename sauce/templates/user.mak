<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists"/>

<%def name="title()">
  ${user} - Profile page
</%def>

<h2>${user} - Profile page</h2>

<p><a href="${tg.url('/user/profile')}">Edit profile</a></p>

% if student:

  <h3>Your events:</h3>
  <ul>
  % for team in student['teams']:
    <li>${team.name} - ${team.lesson.name} (${team.lesson.event.link})</li>
  % endfor
  % for lesson in student['lessons']:
    <li>${lesson.name} (${lesson.event.link})</li>
  % endfor
  </ul>

% elif teacher:

  % if teacher['events']:
    <h3>Your events:</h3>
    <ul>
    % for event in teacher['events']:
      <li>${event.link}</li>
    % endfor
    </ul>
  % endif
  % if teacher['lessons']:
    <h3>Your lessons:</h3>
    <ul>
    % for lesson in teacher['lessons']:
      <li>${lesson.link} (${lesson.event.link})</li>
    % endfor
  % endif
  </ul>

% endif

<h3>Your submissions:</h3>

% if hasattr(c, 'table'):
  <div class="crud_table">
    ${c.table(value=values, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
  </div>
% endif
