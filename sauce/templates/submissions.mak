<%inherit file="local:templates.master"/>

<%def name="title()">
  Submissions
</%def>

<h2>Submissions</h2>

<h3>Your Submissions</h3>

<table>
  <tr>
    <th>ID</th>
    <th>Assignment</th>
    <th>Result</th>
    %for submission in submissions.items:
    <tr>
        <th>${h.link(submission.id, tg.url('/submissions/%d' % submission.id))}</th>
        <td>${h.link(submission.assignment.name, tg.url('/assignments/%d' % submission.assignment.id))}</td>
        <td>
        % if not submission.complete:
          n/a
        % else:
		  % if submission.testrun.result:
		    <span class="green">ok</span>
		  % else:
		    <span class="red">fail</span>
		  </div>
		  % endif
        % endif
        </td>
    </tr>
    %endfor
</table>
  
<p>${submissions.pager('Pages: $link_previous ~2~ $link_next')}</p>


