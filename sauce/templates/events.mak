<%inherit file="local:templates.master" />

<%!
  import string
  import sauce.lib.helpers as h
%>

<%def name="title()">
  Events
</%def>

<div class="page-header">
  <h1>Events</h1>
</div>

<h2>Current events:</h2>

% if events:
  ${list(events)}
  % if hasattr(events, 'pager'):
    <p>${events.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% else:
  <p>No currently active events found.</p>
% endif

##<hr />

% if future_events:
  <h2>Future events:</h2> 
  ${list(future_events)}
  % if hasattr(future_events, 'pager'):
    <p>${future_events.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

% if previous_events:
  <h2>Previous events:</h2> 
  ${list(previous_events)}
  % if hasattr(previous_events, 'pager'):
    <p>${previous_events.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

<%def name="list(events)">

<dl>
  % for event in events:
##    <dt>${h.link(event.name, tg.url('/events/%s' % event.url))} (${event.type | string.capitalize})</dt>
    <dt>${event.link} (${event.type | string.capitalize})
      % if not event.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    <dd>${event.description | n, h.striphtml, h.cut }</dd>
  % endfor
</dl>

</%def>