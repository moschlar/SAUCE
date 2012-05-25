<%inherit file="local:templates.submission" />
<%namespace file="local:templates.submission" import="details,details_judgement" />
<%namespace file="local:templates.lists" name="lists" />

${details(submission)}

% if submission.judgement:

  ${details_judgement(submission.judgement)}

% endif

% if submission.testruns:
  ${lists.testruns(submission.visible_testruns)}
% endif

