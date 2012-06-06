<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists"/>

<%def name="title()">
  ${user} - Profile page
</%def>

<div class="page-header">
  <h1>${user} <small>Profile page</small></h1>
</div>

<p><a href="${tg.url('/user/profile')}" class="btn btn-primary"><i class="icon-user icon-white"></i> Edit profile</a></p>

% if memberships['teams']:
  <h4>Your teams:</h4>
  <ul>
  % for team in memberships['teams']:
    <li>${team.name} - ${team.lesson.name} (${team.lesson.event.link})</li>
  % endfor
  </ul>
% endif
% if memberships['lessons']:
  <h4>Your lessons:</h4>
  <ul>
  % for lesson in memberships['lessons']:
    <li>${lesson.name} (${lesson.event.link})</li>
  % endfor
  </ul>
% endif
% if memberships['events']:
  <h4>Your events:</h4>
  <ul>
  % for event in memberships['events']:
    <li>${event.link}</li>
  % endfor
  </ul>
% endif

<h3>Your 
% if memberships['teams']:
  (and your teammates)
% endif
submissions:</h3>

<div class="crud_table">
  ${c.table(value=values, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
</div>
