<%inherit file="local:templates.master"/>
<%namespace file="local:templates.sheets" name="sheets" />
<%namespace file="local:templates.lists" name="lists" />
<%namespace file="local:templates.misc" import="times_dl" />

<%def name="title()">
  ${event.name}
</%def>



<div class="page-header">
  % if hasattr(request, 'user') and request.user == event.teacher or 'manage' in request.permissions:
    <div class="pull-right">
      <a href="${event.url}/admin/events/${event.id}/edit" class="btn"><i class="icon-pencil"></i>&nbsp;Edit</a>
    </div>
  % endif
  <h1>${event.name} <small>Event</small></h1>
</div>

${self.details(event)}

<%def name="details(event)">

<p class="description">${event.description | n }</p>

% if event.teacher:
  <dl>
    <dt>Contact:</dt>
    <dd>
      <a href="mailto:${event.teacher.email_address}" class="btn btn-mini">
      <i class="icon-envelope"></i>&nbsp;${event.teacher.display_name}</a>
    </dd>
  </dl>
% endif

% if event.type == 'contest':
  ${times_dl(event)}
% endif

  % if event.sheets:
    <h2><a href="${event.url}/sheets">Sheets</a></h2>
    
    % if event.current_sheets:
      <h3>Current sheets</h3>
      ${sheets.list(event.current_sheets)}
    % endif

    % if event.future_sheets:
      <h3>Future sheets</h3>
      ${sheets.list_short(event.future_sheets)}
    % endif

    % if event.previous_sheets:
      <h3>Previous sheets</h3>
      ${sheets.list_short(event.previous_sheets)}
    % endif
  % endif


% if hasattr(request, 'user') and request.user == event.teacher or 'manage' in request.permissions:
  <div class="pull-right">
    <a href="${event.url}/admin/newsitems/?event_id=${event.id}" class="btn"><i class="icon-pencil"></i>&nbsp;Edit</a>
  </div>
% endif
<h2>News</h2>
% if event.news:
  ##TODO
  ##% if request.teacher:
  ##  ${lists.news(event.news)}
  ##% else:
    ${lists.news((news for news in event.news if news.public))}
  ##% endif
% else:
  <p>No news for ${event.name}.</p>
% endif

</%def>
