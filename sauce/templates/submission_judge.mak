<%inherit file="local:templates.submission" />
<%namespace file="local:templates.submission" import="details" />

${details(submission)}

<h2>Judgement</h2>
${c.judgement_form.display(options) | n}

##TODO: Show corrected source code results
##% if compilation:
##  ${details.compilation(compilation)}
##% endif

##% if submission.testruns:
##  ${lists.testruns(submission.testruns)}
##% endif

