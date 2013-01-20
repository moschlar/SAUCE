<%inherit file="local:templates.master"/>

<%def name="title()">
  ${page_title}
</%def>

% if page_header:
  <div class="page-header">
    <h1>${page_header}</h1>
  </div>
% endif

${content | n}