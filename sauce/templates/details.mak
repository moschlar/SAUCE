<%namespace file="local:templates.lists" name="lists" />
<%namespace file="local:templates.misc" import="times_dl" />

<%!
  import string
%>

<%def name="event(event)">

<p class="description">${event.description | n }</p>

% if event.teacher:
  <dl>
    <dt>Contact:</dt>
    <dd><a href="mailto:${event.teacher.email_address}">${event.teacher.display_name}</a></dd>
  </dl>
% endif

% if event.type == 'contest':
  ${times_dl(event)}
% endif

% if event.sheets:
  <h3>Sheets</h3>
  
  % if event.current_sheets:
    <h3>Current sheets</h3>
    ${lists.sheets(event.current_sheets)}
  % endif

  % if event.future_sheets:
    <h3>Future sheets</h3>
    ${lists.sheets_short(event.future_sheets)}
  % endif

  % if event.previous_sheets:
    <h3>Previous sheets</h3>
    ${lists.sheets_short(event.previous_sheets)}
  % endif

  
% endif

% if event.news:
  <h3>News</h3>
  
  ${lists.news(event.news)}
  
% endif

</%def>


<%def name="sheet(sheet)">

<p class="description">${sheet.description | n}</p>

${times_dl(sheet)}

<h3>Assignments:</h3>
${lists.assignments(sheet.assignments)}

</%def>


<%def name="assignment(assignment)">

<p class="description">${assignment.description | n }</p>

<table>
  <tr>
    <th>Start time:</th>
    <th>End time:</th>
  </tr>
  <tr>
    <td>${assignment.start_time.strftime('%x %X')}</td>
    <td>${assignment.end_time.strftime('%x %X')}</td>
  </tr>
</table>

% if assignment.is_active:
  <table><tr>
    <th>Remaining time:</th>
    <td>${h.strftimedelta(assignment.remaining_time)}</td>
  </tr></table>
% else:
  <p>Assignment is not active at the moment.</p>
%endif

##% if request.student:
  % if submissions:
    <h3>Your Submissions</h3>
    <ul>
    % for submission in reversed(submissions):
      <li>${submission.link}
      % if submission.complete:
        % if submission.result:
          <span class="green">(ok)</span>
        % else:
          <span class="red">(failed)</span>
        % endif
      % endif
      </li>
    % endfor
    </ul>
  % endif
  
  % if request.teacher or assignment.is_active:
    <p>${h.link('Submit new solution', '%s/submit' % (assignment.url))}</p>
##  % else:
##    <p>Submissions are already closed.</p>
  % endif
##% endif

% if assignment.timeout:
  <p>General timeout: ${assignment.timeout} seconds</p>
% endif
  % if assignment.visible_tests:
    <h3>Tests</h3>
    % if assignment.visible_tests:
      <table>
        <tr>
          <th>Input</th>
          <th>Output</th>
        </tr>
      % for test in assignment.visible_tests:
        <tr>
          <td><pre class="code">${test.input_data}</pre></td>
          <td><pre class="code">${test.output_data}</pre></td>
        </tr>
      % endfor
    </table>
  % endif
% endif

</%def>

<%def name="submission(submission, source=None)">
  
  % if submission.assignment:
    <p>
     for Assignment ${submission.assignment.link}
    </p>
  % endif

<p>Created: ${submission.created.strftime('%x %X')}, Last modified: ${submission.modified.strftime('%x %X')}</p>

  % if not submission.complete and submission.assignment.is_active:
    <p><a href="${tg.url('/submissions/%d/edit' % submission.id)}">Edit submission</a></p>
  % endif

  <table>
    % if len(submission.assignment.allowed_languages) > 1:
      <tr>
        <th>Language</th>
        <td>${submission.language}</td>
      </tr>
    % endif

    % if submission.complete:
      <tr>
        <th>Test result</th>
        <td>
          % if submission.result:
            <span class="green">ok</span>
          % else:
            <span class="red">fail</span>
          % endif
        </td>
      </tr>
      <tr>
        <th>Runtime</th>
        <td>${submission.runtime}</td>
      </tr>
      % if submission.judgement:
        <tr>
          <th>Grade</th>
          <td>${submission.judgement.grade}</td>
        </tr>
      % endif
    % else:
      <p>Submission not yet submitted.</p>
    % endif
  </table>

  <h3>Source code:</h3>
  % if source:
    <p><a href="${submission.url}/download">Download source</a></p>
    <div id="source_container">${source | n}</div>
  % elif submission.source:
    <p><a href="${submission.url}/download">Download source</a></p>
    <div id="source_container"><pre>${submission.source}</pre></div>
  % else:
    <p>No source code submitted yet.</p>
  % endif
  
</%def>

<%def name="judgement(judgement, corrected_source=None, diff=None)">

  % if judgement.annotations:
  <h4>Annotations:</h4>
    <table>
    % for line, ann in judgement.annotations.iteritems():
      <tr>
        <th>
          <a href="javascript:highline(${line})">Line ${line}</a>
        </th>
        <td>
          ${ann}
        </td>
      </tr>
    % endfor
    </table>
  % endif

  % if judgement.comment:
    <h4>Comment:</h4>
    <p>${judgement.comment}</p>
  % endif

  % if corrected_source:
    <h4>Corrected source code:</h4>
      ${corrected_source | n}
    <h4>Diff</h4>
      ${diff | n}
  % endif

</%def>

<%def name="compilation(compilation)">

  <h3>Compilation result</h3>
  % if compilation.returncode == 0:
    <p>Success</p>
  % else:
    <p>Fail</p>
  % endif
  <table>
  <tr>
    <th>stdout</th><th>stderr</th>
  </tr>
  <tr>
    <td><pre>${compilation.stdout}</pre></td>
    <td><pre>${compilation.stderr}</pre></td>
  </tr>
  </table>

</%def>

