<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists" />

<%def name="title()">
  Assignments
</%def>

<h2>Assignments</h2>

${lists.assignments(assignments)}

