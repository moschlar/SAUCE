<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" name="details"/>

% if event:
  <%def name="body_class()">class="navbar_left"</%def>
% endif

<%def name="title()">
  ${assignment.name} - Assignment
</%def>

<h2>${assignment.name}</h2>

${details.assignment(assignment)}

% if request.teacher:
<h3>Teacher section</h3>
  <h4>Tests:</h4>
  <ul>
  % for test in assignment.tests:
    <li>${test} <a href="${tg.url(assignment.url+'/test/edit/%d'%test.id)}">edit</a> delete</li>
  % endfor
  </ul>
  <a href="${tg.url(assignment.url+'/test/new')}">new</a>
% endif