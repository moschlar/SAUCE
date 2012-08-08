<%inherit file="local:templates.master"/>

<%def name="title()">
  ${heading}
</%def>

<div class="page-header">
  <h1>${heading}</h1>
</div>

${content | n}