<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" name="details"/>

<%def name="title()">
  ${assignment.name} - Assignment
</%def>

<h2>${assignment.name}</h2>

${details.assignment(assignment)}
