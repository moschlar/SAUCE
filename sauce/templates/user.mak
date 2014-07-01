## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

<%inherit file="local:templates.master"/>

<%def name="title()">
  ${user} - Profile page
</%def>

<div class="page-header">
  <h1>${user} <small>Profile page</small></h1>
</div>

<p><a href="${tg.url('/user/profile')}" class="btn btn-primary">
  <i class="icon-user icon-white"></i>&nbsp;Edit profile
</a></p>

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
    <li>
      % if getattr(request, 'user', None) == lesson.tutor:
        <a href="${tg.url('%s/lessons/%d' % (lesson.event.url, lesson.id))}">${lesson.name}</a>
      % else:
        ${lesson.name}
      % endif
      (${lesson.event.link})
    </li>
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

<h3>Your submissions:</h3>

## TODO: Is crud_table still needed?
<div class="crud_table">
  ## TODO: Are the attrs still needed?
  ${c.table(value=values, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
</div>
