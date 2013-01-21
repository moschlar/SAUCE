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
  import sauce.lib.helpers as h
%>

<%def name="title()">
  ${sheet.name} - Assignments
</%def>

<div class="page-header">
  % if getattr(request, 'user', None) == event.teacher or 'manage' in request.permissions:
    <div class="pull-right">
      <a href="${sheet.event.url}/admin/assignments/?sheet_id=${sheet.id}" class="btn"><i class="icon-pencil"></i>&nbsp;Edit</a>
    </div>
  % endif
  <h1>${sheet.name} <small>Assignments</small></h1>
</div>

${self.list(assignments)}
% if hasattr(assignments, 'pager'):
  <p>${assignments.pager('Pages: $link_previous ~2~ $link_next')}</p>
% endif

<%def name="list(assignments)">

<dl>
  %for assignment in assignments:
    <dt>${assignment.link} 
      % if not assignment.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    
    <dd>${assignment.description | n, h.striphtml, h.cut }</dd>
  %endfor
</dl>

</%def>
