<%inherit file="local:templates.master"/>

<%def name="title()">
  Submissions
</%def>

<h2>Submissions</h2>

% if hasattr(c, 'table'):
    <div class="crud_table">
     ${tmpl_context.table(value=value_list, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
    </div>
  % if values:
    % if values['sheets']:
      % for sheet in values['sheets']:
        <h4>${sheet.name}</h4>
        ${tmpl_context.table(value=sheet.submissions, attrs=dict(style="height:200px; border:solid black 3px;")) | n}
      % endfor
    % endif
  % endif
% endif
