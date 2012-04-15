<%inherit file="local:templates.master"/>

<%def name="title()">
  Lesson
</%def>

<%def name="body_class()">class="navbar_left"</%def>

<h2>Lesson</h2>

<h3>Teacher:</h3>
${lesson.teacher}

<h3>Teams:</h3>
<ul>
% for team in lesson.teams:
  <li>${team.name}</li>
% endfor
</ul>

<h4>Add Team</h4>
${c.form(options=options, action=tg.url(lesson.url+'/post')) | n}