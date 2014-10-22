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

<%inherit file="local:templates.master" />

<%!
  import string
  import sauce.lib.helpers as h
%>

<%def name="title()">
  Events
</%def>

<div class="page-header">
  % if getattr(request, 'user', None) or 'manage' in request.permissions:
    <div class="pull-right">
      <a href="/events/request/new" class="btn"><i class="icon-plus"></i>&nbsp;Request new Event</a>
    </div>
  % endif
  <h1>Events</h1>
</div>

<h2>Current events:</h2>

% if events:
  ${list(events)}
  <p>${c.paginators.events.pager('Pages: $link_previous ~2~ $link_next') | n}</p>
% else:
  <p>No currently active events found.</p>
% endif

##<hr />

% if future_events:
  <h2>Future events:</h2> 
  ${list(future_events)}
  <p>${c.paginators.future_events.pager('Pages: $link_previous ~2~ $link_next') | n}</p>
% endif

% if previous_events:
  <h2>Previous events:</h2> 
  ${list(previous_events)}
  <p>${c.paginators.previous_events.pager('Pages: $link_previous ~2~ $link_next') | n}</p>
% endif

<%def name="list(events)">

<dl>
  % for event in events:
##    <dt>${h.link(event.name, tg.url('/events/%s' % event.url))} (${event.type | string.capitalize})</dt>
    <dt>${event.link} (${event.type | string.capitalize})
      % if not event.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    <dd>${event.description | n, h.striphtml, h.cut }</dd>
  % endfor
</dl>

</%def>