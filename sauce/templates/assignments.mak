<%inherit file="local:templates.master" />
<%namespace file="local:templates.lists" name="lists" />

<%def name="title()">
  ${sheet.name} - Assignments
</%def>

<h2>${sheet.name} - Assignments</h2>

${lists.assignments(assignments)}
% if hasattr(assignments, 'pager'):
  <p>${assignments.pager('Pages: $link_previous ~2~ $link_next')}</p>
% endif
