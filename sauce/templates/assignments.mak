<%inherit file="local:templates.master"/>

<%def name="title()">
  Assignments
</%def>

<h2>Assignments</h2>

  <h3>Current Assignments</h3>
  <dl>
      % for assignment in assignments.items:
        <dt>${h.html.tags.link_to(assignment.name, tg.url('/assignments/%d' % assignment.id))}</dt>
        <dd>${assignment.description}</dd>
      % endfor
  </dl>
  <p>${assignments.pager('Pages: $link_previous ~2~ $link_next')}</p>
  
  <h3>Past Assignments</h3>

