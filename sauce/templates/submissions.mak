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
  Submissions
</%def>

<div class="page-header">
  <h1>Submissions</h1>
</div>

<!--
% try:
filters:          ${unicode(filters) | n}
real_filters:     ${unicode(real_filters) | n}
definite_filters: ${unicode(definite_filters) | n}
% except:

% endtry
-->

% if not view:
${c.table(value=values) | n}
% else:

<p>
${h.link_to_unless(view=='by_team', 'by Team', '?view=by_team') }, 
${h.link_to_unless(view=='by_sheet', 'by Sheet', '?view=by_sheet') }, 
${h.link_to_unless(view=='by_student', 'by Student', '?view=by_student') }
</p>

% if hasattr(c, 'table'):
  % if values:
    % if values['sheets']:
      <h3>Sheets:</h3>
      % for sheet in values['sheets']:
        % if sheet.submissions_:
          <h4>${sheet.name}</h4>
          <div class="crud_table">
            ${tmpl_context.table(id='sheet_%d' % sheet.id, value=sheet.submissions_, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
          </div>
        % endif
      % endfor
    % endif
    % if values['teams']:
      <h3>Teams:</h3>
      % for team in values['teams']:
        % if team.submissions_:
          <h4>${team.name}</h4>
          <div class="crud_table">
            ${tmpl_context.table(id='team_%d' % team.id, value=team.submissions_, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
          </div>
        % endif
      % endfor
    % endif
    % if values['students']:
      <h3>Students:</h3>
      % for student in values['students']:
        % if student.submissions_:
          <h4>${student.display_name}</h4>
          <div class="crud_table">
            ${tmpl_context.table(id='student_%d' % student.id, value=student.submissions_, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
          </div>
        % endif
      % endfor
    % endif
  % endif
% endif
%endif
