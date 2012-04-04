<%namespace file="local:templates.lists" import="news_list, sheet_list, assignment_list" />
<%namespace file="local:templates.misc" import="times_dl" />

<%!
  import string
%>

<%def name="event_details(event)">

<p class="description">${event.description | n }</p>

% if event.type == 'contest':
  ${times_dl(event)}
% endif

% if event.sheets:
  <h3>Sheets</h3>
  
  ${sheet_list(event.sheets)}
  
% endif

% if event.news:
  <h3>News</h3>
  
  ${news_list(event.news)}
  
% endif

</%def>


<%def name="sheet_details(sheet)">

<p class="description">${sheet.description | n}</p>

${times_dl(sheet)}

<h3>Assignments:</h3>
${assignment_list(sheet.assignments)}

</%def>