<%inherit file="local:templates.master"/>

<%def name="title()">
  Events
</%def>

<h2>Events</h2>
  <p>Current Events: 
  <table>
      %for event in events.items:
      <tr>
          <td>${h.html.tags.link_to(event.name, tg.url('/events/%d' % event.id))}</td>
          <td>${event.description}</td>
      </tr>
      %endfor
  </table>
  Pages: ${events.pager('$link_previous ~2~ $link_next')}
  </p>

