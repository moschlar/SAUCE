<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" name="details" />

<%def name="title()">
  ${sheet.name}
</%def>

<h2>${sheet.name}</h2>

${details.sheet(sheet)}
