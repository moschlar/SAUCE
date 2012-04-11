<%inherit file="local:templates.master" />
<%namespace file="local:templates.lists" name="lists" />

<%def name="title()">
  Events
</%def>

<h2>Events</h2>

<h3>Current events:</h3>

% if events:
  ${lists.events(events)}
  % if hasattr(events, 'pager'):
    <p>${events.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% else:
  <p>No currently active events found.</p>
% endif

##<hr />

% if future_events:
  <h3>Future events:</h3> 
  ${lists.events(future_events)}
  % if hasattr(future_events, 'pager'):
    <p>${future_events.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

% if previous_events:
  <h3>Previous events:</h3> 
  ${lists.events(previous_events)}
  % if hasattr(previous_events, 'pager'):
    <p>${previous_events.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif
