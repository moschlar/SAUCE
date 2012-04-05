<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" import="assignment_details" />

% if event:
<%def name="body_class()">navbar_left</%def>
% endif

<%def name="title()">
  ${assignment.name} - Assignment
</%def>

<h2>${assignment.name}</h2>

${assignment_details(assignment)}
