<%inherit file="local:templates.master"/>

<%def name="title()">
  Submission
</%def>

<h2>Submission</h2>

<h3>Submission for Assignment: ${h.html.tags.link_to(submission.assignment.title, tg.url('/assignments/%d' % submission.assignment.id))}</h3>

<p>Language: ${submission.language}, Compiler: ${submission.language.compiler}</p>

<h4>Source code:</h4>
<pre>
${submission.source}
</pre>

