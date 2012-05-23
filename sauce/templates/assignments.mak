<%inherit file="local:templates.master" />

<%!
  import sauce.lib.helpers as h
%>

<%def name="title()">
  ${sheet.name} - Assignments
</%def>

<div class="page-header">
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
