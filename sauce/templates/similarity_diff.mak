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

<%def name="title()">
  Similarity ${view}
</%def>

<%def name="submission_details(submission)">
  <dl class="dl-horizontal">
    <dt>Submission:</dt>
    <dd>
      <a href="${submission.url}" style="color: white">
        <span class="badge ${'' if submission.result is None else ('badge-success' if submission.result else 'badge-error')}">
          ${submission.id}
        </span>
      </a>
    </dd>
  </dl>
  <dl class="dl-horizontal">
    <dt>User:</dt>
        <dd>${submission.user.display_name}</dd>
    % if submission.team:
      <dt>Team:</dt>
          <dd>${submission.team}</dd>
    % endif
    <dt>Created:</dt>
        <dd title="${h.strftime(submission.created, False)}">${h.strftime(submission.created, True)}</dd>
    <dt>Last modified:</dt>
        <dd title="${h.strftime(submission.modified, False)}">${h.strftime(submission.modified, True)}</dd>
  </dl>
</%def>

<div class="page-header">
  <h1>Similarity ${view}
    % if assignment:
      <small>for Assignment: ${assignment.link}</small>
    % endif
  </h1>
</div>

<div class="row">
  <div class="offset1 span5"><div class="">
    ${submission_details(a)}
  </div></div>
  <div class="span5"><div class="">
    ${submission_details(b)}
  </div></div>
</div>

<div class="row">
  <div class="offset4 span4">
    <div class="" style="text-align: center;">
      <dl class="dl-horizontal">
        <dt>Similarity value:</dt>
        <dd style="color: ${c.rgb(x)}">${'%.2f' % (1 - x)}</dd>
      </dl>
    </div>
  </div>
</div>

<div class="row">
  <div class="span12">
    ${c.source_display.display(source, id='source_diff', compound_id='source_diff%d',
      mode='diff', lineNumbers=False) | n}
  </div>
</div>
