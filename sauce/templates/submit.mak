<%inherit file="local:templates.master"/>

<%def name="title()">
  Submission
</%def>

<h2>Submission</h2>

<h3>Submission for Assignment: ${h.html.tags.link_to(assignment.title, tg.url('/assignments/%d' % assignment.id))}</h3>

<p>Language: </p>

<h4>Source code:</h4>
<pre>

</pre>

