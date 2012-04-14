<%inherit file="local:templates.master"/>

<%def name="title()">
  % if heading:
    ${heading}
  % else:
    ${page.capitalize()}
  % endif
</%def>

<h2>
  % if heading:
    ${heading}
  % else:
    ${page.capitalize()}
  % endif
</h2>

${c.form(options, child_args=child_args, action=action) | n}