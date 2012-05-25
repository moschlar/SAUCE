<%inherit file="local:templates.submission" />
<%namespace file="local:templates.submission" import="details" />
<%namespace file="local:templates.lists" name="lists" />

${details(submission)}

${c.form(c.options, child_args=c.child_args) | n}

##% if submission.judgement:
##  ${details.judgement(submission.judgement, corrected_source, diff)}
##% endif

% if compilation:
  ${details.compilation(compilation)}
% endif

% if submission.testruns:
  ${lists.testruns(submission.testruns)}
% endif

