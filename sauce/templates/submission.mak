<%inherit file="local:templates.master"/>

<%def name="title()">
  SAUCE - Submission
</%def>

${parent.sidebar_top()}
<h2>SAUCE - Submission</h2>

<h3>Submission for Assignment: ${submission.assignment.title}</h3>

<p>Language: ${submission.language}, Compiler: ${submission.language.compiler}</p>

<h4>Source code:</h4>
<pre>
${submission.source}
</pre>

<%def name="sidebar_bottom()"></%def>
