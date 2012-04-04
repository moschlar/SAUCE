<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" import="sheet_list, sheet_list_short" />

% if event:
<%def name="body_class()">navbar_left</%def>
% endif

<h2>Sheets</h2>

<h3>Current sheets</h3>

${sheet_list(all_sheets.current)}

% if all_sheets.future:
  <h3>Future sheets</h3>
  ${sheet_list_short(all_sheets.future)}
% endif

% if all_sheets.previous:
  <h3>Previous sheets</h3>
  ${sheet_list_short(all_sheets.previous)}
% endif
