<%inherit file="local:templates.master"/>

<%def name="title()">
  ${user}
</%def>

<h2>User: ${user}</h2>

${c.form(user) | n}