<%inherit file="local:templates.master"/>
<%namespace file="local:templates.submission" import="details" />
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

