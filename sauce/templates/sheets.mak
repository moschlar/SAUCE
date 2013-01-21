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
<%namespace file="local:templates.assignments" name="assignments" />
<%namespace file="local:templates.misc" import="times_dl" />

<%!
  import sauce.lib.helpers as h
%>

<%def name="title()">
  ${event.name} - Sheets
</%def>

<div class="page-header">
  % if getattr(request, 'user', None) == event.teacher or 'manage' in request.permissions:
    <div class="pull-right">
      <a href="${event.url}/admin/sheets/" class="btn"><i class="icon-pencil"></i>&nbsp;Edit</a>
    </div>
  % endif
  <h1>${event.name} <small>Sheets</small></h1>
</div>

% if current_sheets:
  <h2>Current sheets</h2>
  ${list(current_sheets)}
  % if hasattr(current_sheets, 'pager'):
    <p>${current_sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

% if future_sheets:
  <h2>Future sheets</h2>
  ${list(future_sheets)}
  % if hasattr(future_sheets, 'pager'):
    <p>${future_sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

% if previous_sheets:
  <h2>Previous sheets</h2>
  ${list(previous_sheets)}
  % if hasattr(previous_sheets, 'pager'):
    <p>${previous_sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

<%def name="list_short(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${sheet.link}
      % if not sheet.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    <dd>
      <p>${sheet.description | n, h.striphtml, h.cut }</p>
    </dd>
  % endfor
</dl>

</%def>

<%def name="list(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${sheet.link}
      % if not sheet.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    <dd>
      <p>${sheet.description | n, h.striphtml, h.cut }</p>
      ${times_dl(sheet)}

      % if sheet.public:
        <h4><a href="${tg.url('%s/assignments' % sheet.url)}">Assignments</a>
          <span class="badge">${len(sheet.assignments)}</span></h4>
        ${assignments.list(sheet.assignments)}
      % endif
    </dd>
  % endfor
</dl>

</%def>
