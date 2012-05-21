<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" name="details" />
<%namespace file="local:templates.lists" name="lists" />



<%def name="title()">
  Submission
</%def>

<h2>Submission 
% if submission and hasattr(submission, 'id'):
  ${submission.id}
% endif
</h2>

${details.submission(submission)}

% if submission.judgement:

  ${details.judgement(submission.judgement)}

% endif

% if submission.testruns:
  ${lists.testruns(submission.visible_testruns)}
% endif

