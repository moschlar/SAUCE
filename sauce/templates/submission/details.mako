<%inherit file="/base.mako" />

<h1>System for AUtomated Code Evaluation</h1>
<h2>${c.site}</h2>

% if hasattr(c, 'submission'):
  <h3>Assignment: ${c.submission.assignment.title}</h3>
  <p>${c.submission.assignment.description}</p>
  
  <h4>Submission source:</h4>
  <pre>
  ${c.submission.source}
  </pre>
  
  <h4>Submission test run:</h4>
  % if len(c.submission.testruns):
    % for testrun in sorted(c.submission.testruns, key=lambda run: run.date):
      <p>${testrun.date} ${testrun.result}</p>
    % endfor
  % else:
    <p>No test has been run yet<br />
    ${h.link_to('Test',url(controller='submission', id=c.submission.id, action='test'))}</p>
  % endif
% endif