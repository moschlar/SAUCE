<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" import="assignment_list" />

% if event:
  <%def name="body_class()">navbar_left</%def>
% endif

<%def name="title()">
  Assignments
</%def>

<h2>Assignments</h2>

${assignment_list(assignments)}

