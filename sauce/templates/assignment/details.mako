<%inherit file="/base.mako" />

<h1>System for AUtomated Code Evaluation</h1>
<h2>${c.site}</h2>

% if hasattr(c, 'assignment'):
  <h3>Assignment: ${c.assignment.title}</h3>
  <p>${c.assignment.description}</p>
  
  <p><a href="${url(controller='assignment', action='submission', id=c.assignment.id)}">Submit solution</a></p>
  
  % if c.assignment.visible_tests:
    <h4>Tests:</h4>
    % for test in c.assignment.visible_tests:
      <h5>Input:</h5>
        <pre>${test.input}</pre>
      <h5>Output:</h5>
        <pre>${test.output}</pre>
    % endfor
  % endif
% endif