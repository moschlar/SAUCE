<%inherit file="local:templates.master"/>

<%def name="title()">
  SAUCE - Assignments
</%def>

${parent.sidebar_top()}
<h2>SAUCE - Assignments</h2>
  ##${dir(assignments)}
  ##${dir(h.html)}
  ${tg.url('/assignments', dict(id=2))}
  <p>Current Assignments: 
  <table>
      %for assignment in assignments.items:
      <tr>
          <td>${h.html.tags.link_to(assignment.title, tg.url('/assignment/%d' % assignment.id))}</td>
          <td>${assignment.description}</td>
      </tr>
      %endfor
  </table>
  Pages: ${assignments.pager('$link_previous ~2~ $link_next')}
  </p>


<%def name="sidebar_bottom()"></%def>
