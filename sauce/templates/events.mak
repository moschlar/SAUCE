<%inherit file="local:templates.master"/>

<%def name="title()">
  Events
</%def>

<h2>Events</h2>

%if events:
  <h3 class="events">Current Events</h3>
    <dl class="events">
      %for event in events.items:
        <dt>${h.link(event.name, tg.url('/events/%d' % event.id))}</dt>
        <dd>${event.description | n, h.striphtml }</dd>
      %endfor
    </dl>
  <p>${events.pager('Pages: $link_previous ~2~ $link_next')}</p>
% endif

% if past_events:
  <h3 class="past_events">Past Events</h3>
    <dl class="past_events">
      %for event in past_events.items:
        <dt>${h.link(event.name, tg.url('/events/%d' % event.id))}</dt>
        <dd>${event.description | n, h.striphtml }</dd>
      %endfor
    </dl>
  <p>${past_events.pager('Pages: $link_previous ~2~ $link_next')}</p>
% endif