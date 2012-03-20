<%inherit file="local:templates.master"/>

<%def name="title()">
  Submission
</%def>

<h2>Submission 
% if submission and hasattr(submission, 'id'):
  ${submission.id}
% endif
</h2>

<p>
% if assignment:
for Assignment: ${h.link(assignment.name, tg.url('/assignments/%d' % assignment.id))}
% endif
</p>


% if not submission.complete:
  ${c.form(c.options, child_args=c.child_args) | n}
% else:
  <div>
  <table>
    <tr>
      <th>Result</th>
      <td>
        % if submission.testrun.result:
          <span class="green">ok</span>
        % else:
          <span class="red">fail</span>
        % endif
      </td>
    </tr>
    <tr>
      <th>Language</th>
      <td>${submission.language}</td>
    </tr>
    <tr>
      <th>Runtime</th>
      <td>&nbsp;</td>
    </tr>
  </table>
   
  <h3>Source code</h3>
  <pre class="code">${submission.source}</pre>

% endif

% if compilation:
  <h3>Compilation result</h3>
  % if compilation.returncode == 0:
  <p>Success</p>
  % else:
  <p>Fail</p>
  % endif
  <table>
  <tr><th>stdout</th><th>stderr</th></tr>
  <tr><td><pre>${compilation.stdout}</pre></td><td><pre>${compilation.stderr}</pre></td></tr>
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
  <tr><th>Given input</th><th>Expected stdout</th><th>Real stdout</th><th>Real stderr</th></tr>
  <tr><td><pre>${testrun.test.input}</pre></td><td><pre>${testrun.test.output}</pre></td><td><pre>${testrun.process.stdout}</pre></td>
  <td><pre>${testrun.process.stderr}</pre></td></tr>
  </table>
  % endfor
% endif
  