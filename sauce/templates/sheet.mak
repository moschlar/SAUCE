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
<%namespace file="local:templates.assignments" name="assignments" />
<%namespace file="local:templates.misc" import="times_dl" />

<%def name="title()">
  ${sheet.name}
</%def>

<div class="page-header">
  % if getattr(request, 'user', None) == event.teacher or 'manage' in request.permissions:
    <div class="pull-right">
      <a href="${sheet.event.url}/admin/sheets/${sheet.id}/edit" class="btn"><i class="icon-pencil"></i>&nbsp;Edit</a>
    </div>
  % endif
  <h1>${sheet.name} <small>Sheet</small></h1>
</div>

${self.details(sheet)}

<%def name="details(sheet)">

<p class="description">${sheet.description | n}</p>

${times_dl(sheet)}

<h2><a href="${sheet.url}/assignments">Assignments:</a> <span class="badge">${len(sheet.assignments)}</span></h2>

${assignments.list(sheet.assignments)}

</%def>
