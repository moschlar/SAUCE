<%inherit file="local:templates.master"/>

<%def name="title()">
  SAUCE - Submissions
</%def>

${parent.sidebar_top()}
<h2>SAUCE - Submissions</h2>
  ##${dir(submissions)}
  ##${dir(h.html)}
  ${tg.url('/submissions', dict(id=2))}
  <p>Current submissions: 
  <table>
      %for submission in submissions.items:
      <tr>
          <td>${h.html.tags.link_to(submission.title, tg.url('/submissions/%d' % submission.id))}</td>
          <td>${submission.description}</td>
      </tr>
      %endfor
  </table>
  Pages: ${submissions.pager('$link_previous ~2~ $link_next')}
  </p>


<%def name="sidebar_bottom()"></%def>
