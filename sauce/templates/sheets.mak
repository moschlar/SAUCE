<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists" />

% if event:
  <%def name="body_class()">navbar_left</%def>
% endif

<h2>${event.name} - Sheets</h2>

% if sheets:
  <h3>Current sheets</h3>
  ${lists.sheets(sheets)}
  % if hasattr(sheets, 'pager'):
    <p>${sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

% if future_sheets:
  <h3>Future sheets</h3>
  ${lists.sheets_short(future_sheets)}
  % if hasattr(future_sheets, 'pager'):
    <p>${future_sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

% if previous_sheets:
  <h3>Previous sheets</h3>
  ${lists.sheets_short(previous_sheets)}
  % if hasattr(previous_sheets, 'pager'):
    <p>${previous_sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif
