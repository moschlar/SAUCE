<%inherit file="local:templates.master"/>
<%namespace file="local:templates.submission" import="details,details_judgement" />
<%namespace file="local:templates.lists" name="lists" />

<%def name="title()">
<%
  try:
    heading = 'Submission %d' % submission.id
  except:
    heading = 'Submission'
  %>
  ${heading}
</%def>

<div class="page-header">
  <h1>${self.title()}
    % if submission.assignment:
      <small>for Assignment: ${submission.assignment.link}</small>
    % endif
  </h1>
</div>

${details(submission)}

% if submission.judgement:

  ${details_judgement(submission.judgement)}

% endif

% if submission.testruns:
  ${lists.testruns(submission.visible_testruns)}
% endif

