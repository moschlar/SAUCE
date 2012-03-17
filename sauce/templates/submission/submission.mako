<%inherit file="/base.mako" />

<h1>System for AUtomated Code Evaluation</h1>
<h2>${c.site}</h2>

<h3>Assignment: ${c.assignment.title}</h3>
<p>${c.assignment.description}</p>

<p>
${h.form(url(controller='submission', action='submit'))}
  ${h.hidden('assignment', c.assignment.id)}
  ${h.textarea('code', 'Paste your source code here...')} <br />
  Language: ${h.select('language', 0, ((l.id,l.name) for l in c.assignment.allowed_languages))} <br />
  ${h.submit('submit', 'Submit')} <br />
${h.end_form()}
</p>
