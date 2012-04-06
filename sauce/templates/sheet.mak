<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" import="sheet_details" />

% if event:
  <%def name="body_class()">navbar_left</%def>
% endif

<%def name="title()">
  Sheet
</%def>

<h2>${sheet.name}</h2>

${sheet_details(sheet)}