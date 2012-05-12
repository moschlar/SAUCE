<%inherit file="local:templates.master"/>

<%def name="title()">
  Submissions
</%def>

<h2>Submissions</h2>

<p>
${h.link_to_unless(view=='by_sheet', 'by Sheet', '?view=by_sheet') }, 
${h.link_to_unless(view=='by_team', 'by Team', '?view=by_team') }, 
${h.link_to_unless(view=='by_student', 'by Student', '?view=by_student') }
</p>

% if hasattr(c, 'table'):
##    <div class="crud_table">
##     ${tmpl_context.table(value=value_list, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
##    </div>
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
