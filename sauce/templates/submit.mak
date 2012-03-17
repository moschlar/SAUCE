<%inherit file="local:templates.master"/>

<%def name="title()">
  Submission
</%def>

<h2>Submission</h2>

<h3>Submission for Assignment: ${h.html.tags.link_to(assignment.title, tg.url('/assignments/%d' % assignment.id))}</h3>

${c.form(child_args=dict(language=dict(options=[(l.id, l.name) for l in assignment.allowed_languages]))) | n}

