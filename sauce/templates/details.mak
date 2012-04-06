<%namespace file="local:templates.lists" import="news_list, sheet_list, assignment_list, sheet_list_short" />
<%namespace file="local:templates.misc" import="times_dl" />

<%!
  import string
%>

<%def name="event_details(event)">

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
    ${sheet_list(event.current_sheets)}
  % endif

  % if event.future_sheets:
    <h3>Future sheets</h3>
    ${sheet_list_short(event.future_sheets)}
  % endif

  % if event.previous_sheets:
    <h3>Previous sheets</h3>
    ${sheet_list_short(event.previous_sheets)}
  % endif

  
% endif

% if event.news:
  <h3>News</h3>
  
  ${news_list(event.news)}
  
% endif

</%def>


<%def name="sheet_details(sheet)">

<p class="description">${sheet.description | n}</p>

${times_dl(sheet)}

<h3>Assignments:</h3>
${assignment_list(sheet.assignments)}

</%def>


<%def name="assignment_details(assignment)">

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
  <p>Event is finished.</p>
%endif

% if request.student:
  % if submissions:
    <h3>Your Submissions</h3>
    <ul>
    % for submission in reversed(submissions):
      <li>${h.html.tags.link_to(submission, tg.url('/submissions/%d' % submission.id))}
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
  
  % if assignment.is_active:
    <p>${h.html.tags.link_to('Submit new solution', 
        tg.url('/events/%s/sheets/%d/assignments/%d/submit' % (assignment.sheet.event.url, assignment.sheet.id, assignment.id)))}</p>
  % else:
    <p>Submissions are already closed</p>
  % endif
% endif

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

