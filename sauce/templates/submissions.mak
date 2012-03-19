<%inherit file="local:templates.master"/>

<%def name="title()">
  Submissions
</%def>

<h2>Submissions</h2>

  <p>Current submissions: 
  <table>
    <tr>
      <th>ID</th>
      <th>Assignment</th>
      <th>Last Result</th>
      %for submission in submissions.items:
      <tr>
          <th>${h.html.tags.link_to(submission.id, tg.url('/submissions/%d' % submission.id))}</th>
          <td>${submission.assignment.name}</td>
          <td>
          % if not submission.testruns:
            Never run
          % else:
            ${submission.testruns[0].result}
          % endif
          </td>
      </tr>
      %endfor
  </table>
  ${submissions.pager('Pages: $link_previous ~2~ $link_next')}
  </p>


