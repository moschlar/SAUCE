<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" name="details" />

% if event:
  <%def name="body_class()">class="navbar_left"</%def>
% endif

<%def name="title()">
  Sheet
</%def>

<h2>${sheet.name}</h2>

${details.sheet(sheet)}