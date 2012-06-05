<%inherit file="local:templates.submission" />
<%namespace file="local:templates.submission" import="details,details_judgement" />

${details(submission)}

% if submission.judgement:
  <h2>Judgement</h2>
  ${details_judgement(submission.judgement)}
% endif

