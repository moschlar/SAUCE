<%inherit file="local:templates.master"/>

<%def name="title()">
  Submissions
</%def>

<h2>Submissions</h2>
  ##${dir(submissions)}
  ##${dir(h.html)}
  ##${tg.url('/submissions', dict(id=2))}
  <p>Current submissions: 
  <table>
      %for submission in submissions.items:
      <tr>
          <td>${h.html.tags.link_to(submission.id, tg.url('/submissions/%d' % submission.id))}</td>
          <td>${submission.assignment.title}</td>
      </tr>
      %endfor
  </table>
  Pages: ${submissions.pager('$link_previous ~2~ $link_next')}
  </p>


