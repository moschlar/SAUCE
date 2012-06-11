<%inherit file="local:templates.master"/>
<%namespace file="local:templates.assignments" name="assignments" />
<%namespace file="local:templates.misc" import="times_dl" />

<%def name="title()">
  ${sheet.name}
</%def>

<div class="page-header">
  <h1>${sheet.name} <small>Sheet</small></h1>
</div>

${self.details(sheet)}

<%def name="details(sheet)">

<p class="description">${sheet.description | n}</p>

${times_dl(sheet)}

<h2><a href="${sheet.url}/assignments">Assignments:</a> <span class="badge">${len(sheet.assignments)}</span></h2>

${assignments.list(sheet.assignments)}

</%def>
