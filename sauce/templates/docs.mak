<%inherit file="local:templates.master"/>

<%def name="title()">
  ${heading}
</%def>

${content | n}