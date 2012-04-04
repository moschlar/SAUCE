<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" import="event_list" />

<%def name="title()">
  Events
</%def>

<h2>Events</h2>


<h3>Current events:</h3> 
% if events:
  ${event_list(events)}
  % if hasattr(events, 'pager'):
    <p>${events.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% else:
  <p>No currently active events found.</p>
% endif

% if future_events:
  <h3>Future events:</h3> 
  ${event_list(future_events)}
  <p>${future_events.pager('Pages: $link_previous ~2~ $link_next')}</p>
% endif

% if previous_events:
  <h3>Previous events:</h3> 
  ${event_list(previous_events)}
  <p>${previous_events.pager('Pages: $link_previous ~2~ $link_next')}</p>
% endif
