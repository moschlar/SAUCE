<%inherit file="local:templates.master"/>

% if breadcrumbs:
  <%def name="body_class()">navbar_left</%def>
% endif

<%def name="title()">
  Submission
</%def>

<%def name="headers()">
  <style type="text/css">
    ${style | n}
  </style>
  <script type="text/javascript">
    function highline(number) {
      var high = document.getElementsByClassName("hll");
      for (var i=0; i < high.length; ++i) {
        high[i].classList.remove("hll");
      }
      var line = document.getElementsByClassName("line-"+number);
      for (var j=0; j < line.length; ++j) {
        line[j].classList.add("hll");
      }
    }
  </script>
</%def>

<h2>Submission 
% if submission and hasattr(submission, 'id'):
  ${submission.id}
% endif
</h2>

% if submission.assignment:
<p>
for Assignment ${submission.assignment.link}
</p>
% endif

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
% endif
</table>

% if source:
  <h3>Source code:</h3>
  ${source | n}
% else:
  <p>No source code submitted yet.</p>
% endif



% if submission.judgement:

  % if submission.judgement.annotations:
  <h4>Annotations:</h4>
    <table>
    % for line, ann in submission.judgement.annotations.iteritems():
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

  % if submission.judgement.comment:
    <h4>Comment:</h4>
    <p>${submission.judgement.comment}</p>
  % endif

  % if corrected_source:
    <h4>Corrected source code:</h4>
      ${corrected_source | n}
    <h4>Diff</h4>
      ${diff | n}
  % endif

% endif

% if compilation:
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
% endif

% if testruns:
  <h3>Testrun results</h3>
  % for testrun in testruns:
    % if testrun.result:
      <p>Success</p>
    % else:
      <p>Fail</p>
    % endif
      <table>
      <tr>
        <th>Given input</th>
        <th>Expected stdout</th>
        <th>Real stdout</th>
        <th>Real stderr</th>
      </tr>
      <tr>
        <td><pre>${testrun.test.input_data}</pre></td>
        <td><pre>${testrun.test.output_data}</pre></td>
        <td><pre>${testrun.output_data}</pre></td>
        <td><pre>${testrun.error_data}</pre></td>
      </tr>
    </table>
  % endfor
% endif

