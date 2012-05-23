<%inherit file="local:templates.master"/>

<%
try:
  heading
except:
  heading = page.capitalize()
%>

<%def name="title()">
  ${heading}
</%def>

<div class="page-header">
  <h1>${heading}</h1>
</div>

${c.form(options, child_args=child_args, action=action) | n}