<%inherit file="local:templates.master"/>

<%def name="title()">
  Events
</%def>

<h2>Events</h2>
  <h3>Current Events</h3>
  <dl>
      %for event in events.items:
        <dt>${h.html.tags.link_to(event.name, tg.url('/events/%d' % event.id))}</dt>
        <dd>${event.description}</dd>
      %endfor
  </dl>
  <p>${events.pager('Pages: $link_previous ~2~ $link_next')}</p>
  
  <h3>Past Events</h3>
