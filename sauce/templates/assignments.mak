<%inherit file="local:templates.master"/>

<%def name="title()">
  Assignments
</%def>

<h2>Assignments</h2>
  ##${dir(assignments)}
  ##${dir(h.html)}
  ##${tg.url('/assignments', dict(id=2))}
  <p>Current Assignments: 
  <table>
      %for assignment in assignments.items:
      <tr>
          <td>${h.html.tags.link_to(assignment.name, tg.url('/assignments/%d' % assignment.id))}</td>
          <td>${assignment.description}</td>
      </tr>
      %endfor
  </table>
  ${assignments.pager('Pages: $link_previous ~2~ $link_next')}
  </p>

