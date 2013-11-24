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
<%namespace file="local:templates.misc" import="times_dl" />

<%def name="title()">
  ${assignment.name}
</%def>

<div class="page-header">
  % if getattr(request, 'user', None) in event.teachers or 'manage' in request.permissions:
    <div class="pull-right">
      <a href="${assignment.sheet.event.url}/admin/assignments/${assignment.id}/edit" class="btn"><i class="icon-pencil"></i>&nbsp;Edit</a>
    </div>
  % endif
  <h1>${assignment.name} <small>Assignment</small></h1>
</div>

${self.details(assignment)}

<%def name="details(assignment)">

<p class="description">${assignment.description | n }</p>

${times_dl(assignment)}

% if request.allowance(assignment):
  % if assignment.lti or assignment.event.lti:
    <%
      from tg import config
    %>
    % if config.features.get('lti', False):
      <dl>
        <dt>LTI tool provider URL:</dt>
        <dd><pre>${tg.url('/lti/%d/' % assignment.id, qualified=True)}</pre></dd>
      </dl>
    % endif
  % endif
% endif

% if assignment.timeout:
  <dl>
    <dt>General test timeout:</dt>
    <dd>${assignment.timeout} seconds</dd>
  </dl>
% endif

  % if request.user and (assignment.is_active or request.allowance(assignment)):
    <p>
    % if submissions:
      <div class="modal hide fade" id="submitModal">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal">×</button>
          <h3>Are you sure?</h3>
        </div>
        <div class="modal-body">
          <p>
            You already made a Submission for this Assignment,
            are you sure you want to create another one?
          </p>
        </div>
        <div class="modal-footer">
          <a href="#" class="btn" data-dismiss="modal">Cancel</a>
          <a href="${tg.url('%s/submit' % (assignment.url))}" class="btn btn-primary">Submit new solution</a>
        </div>
      </div>
      <a href="#submitModal" data-toggle="modal" class="btn btn-primary">Submit new solution</a>
    % else:
      <a href="${tg.url('%s/submit' % (assignment.url))}" class="btn btn-primary">Submit new solution</a>
    % endif
    </p>
  % endif

% if request.user:
  <div class="crud_table">
    ${c.table(value=values, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
  </div>
% endif

% if assignment.visible_tests:
  <h2>Tests</h2>
    <table class="table table-bordered table-condensed test-and-result-table">
    % for test in assignment.visible_tests:
      % if test.argv:
        <tr>
          <th>Command line arguments</th>
          <td><pre>${test.argv}</pre></td>
        </tr>
      % endif
      <tr>
        <th>Given input</th>
        <td><pre>${test.input_data}</pre></td>
      </tr>
      <tr>
        <th>Expected output</th>
        <td><pre>${test.output_data}</pre></td>
      </tr>
    % endfor
  </table>
% endif

</%def>

