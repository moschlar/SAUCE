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
<%namespace file="local:templates.sheets" name="sheets" />
<%namespace file="local:templates.news" name="news" />
<%namespace file="local:templates.misc" import="times_dl" />

<%def name="title()">
  ${event.name}
</%def>



<div class="page-header">
  % if getattr(request, 'user', None) in event.teachers or 'manage' in request.permissions:
    <div class="pull-right">
      <a href="${event.url}/admin/events/${event.id}/edit" class="btn"><i class="icon-pencil"></i>&nbsp;Edit</a>
    </div>
  % endif
  <h1>${event.name} <small>Event</small></h1>
</div>

${self.details(event)}

<%def name="details(event)">

<p class="description">${event.description or u'' | n }</p>

% if event.teachers:
  <dl>
    <dt>Contact:</dt>
    <dd>
    % for teacher in event.teachers:
      <a href="mailto:${teacher.email_address}" class="btn btn-mini">
      <i class="icon-envelope"></i>&nbsp;${teacher.display_name}</a>
    % endfor
    </dd>
  </dl>
% endif

% if event.type == 'contest':
  ${times_dl(event)}
% endif


% if getattr(request, 'user', None):

  % if request.user in set(event.members) | set(event.tutors):

    You are already enrolled for this event.

  % else:

    % if event.enroll:

      <a href="${tg.url('%s/enroll' % (event.url))}" class="btn btn-primary" title="${'Password required' if event.password else ''}">
        Enroll for this ${event.type.title()}
      </a>

    % endif

  % endif

% endif

  % if event.sheets:
    <h2><a href="${event.url}/sheets">Sheets</a></h2>
    
    % if event.current_sheets:
      <h3>Current sheets</h3>
      ${sheets.list(event.current_sheets)}
    % endif

    % if event.future_sheets:
      <h3>Future sheets</h3>
      ${sheets.list_short(event.future_sheets)}
    % endif

    % if event.previous_sheets:
      <h3>Previous sheets</h3>
      ${sheets.list_short(event.previous_sheets)}
    % endif
  % endif


% if getattr(request, 'user', None) in event.teachers or 'manage' in request.permissions:
  <div class="pull-right">
    <a href="${event.url}/admin/newsitems/?event_id=${event.id}" class="btn"><i class="icon-pencil"></i>&nbsp;Edit</a>
  </div>
% endif
<h2>News</h2>
% if event.news:
  ##TODO
  ##% if request.teachers:
  ##  ${news.list(event.news)}
  ##% else:
    ${news.list((_news for _news in event.news if _news.public))}
  ##% endif
% else:
  <p>No news for ${event.name}.</p>
% endif

</%def>
