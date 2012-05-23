<%inherit file="local:templates.master" />
<%namespace file="local:templates.assignments" name="assignments" />
<%namespace file="local:templates.misc" import="times_dl" />

<%!
  import sauce.lib.helpers as h
%>

<%def name="title()">
  ${event.name} - Sheets
</%def>

<div class="page-header">
  <h1>${event.name} <small>Sheets</small></h1>
</div>

% if current_sheets:
  <h2>Current sheets</h2>
  ${list(current_sheets)}
  % if hasattr(current_sheets, 'pager'):
    <p>${current_sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

% if future_sheets:
  <h2>Future sheets</h2>
  ${list(future_sheets)}
  % if hasattr(future_sheets, 'pager'):
    <p>${future_sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

% if previous_sheets:
  <h2>Previous sheets</h2>
  ${list(previous_sheets)}
  % if hasattr(previous_sheets, 'pager'):
    <p>${previous_sheets.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

<%def name="list_short(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${sheet.link}
      % if not sheet.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    <dd>
      <p>${sheet.description | n, h.striphtml, h.cut }</p>
    </dd>
  % endfor
</dl>

</%def>

<%def name="list(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${sheet.link}
      % if not sheet.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    <dd>
      <p>${sheet.description | n, h.striphtml, h.cut }</p>
      ${times_dl(sheet)}

      % if sheet.public:
        <h4><a href="${tg.url('%s/assignments' % sheet.url)}">Assignments</a>
          <span class="badge">${len(sheet.assignments)}</span></h4>
        ${assignments.list(sheet.assignments)}
      % endif
    </dd>
  % endfor
</dl>

</%def>
