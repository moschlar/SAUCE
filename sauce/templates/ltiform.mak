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

<%inherit file="local:templates.only"/>

<%def name="title()">
  ${assignment.name}
</%def>

<div class="page-header">
  <h1>${assignment.name} <small>Assignment</small></h1>
</div>

<p class="description">${assignment.description | n }</p>

<dl class="dl-horizontal">
  <dt>User:</dt>
  <dd>${submission.user.display_name}</dd>

  <dt>Created:</dt>
  <dd title="${h.strftime(submission.created, False)}">${h.strftime(submission.created, True)}</dd>
  <dt>Last modified:</dt>
  <dd title="${h.strftime(submission.modified, False)}">${h.strftime(submission.modified, True)}</dd>
</dl>

${c.form.display(submission) | n}
