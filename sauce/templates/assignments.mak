<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists" />

% if event:
  <%def name="body_class()">class="navbar_left"</%def>
% endif

<%def name="title()">
  Assignments
</%def>

<h2>Assignments</h2>

${lists.assignments(assignments)}

