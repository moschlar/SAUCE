<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists"/>

##% if event:
##  <%def name="body_class()">class="navbar_left"</%def>
##% endif

<%def name="title()">
  ${user}
</%def>

<h2>User: ${user}</h2>

<a href="${tg.url('/user/profile')}">Show/edit profile</a>

% if student:

  <h3>Events:</h3>
  <dl>
  % for (ev,le,te) in student['ev_le_te']:
    <dt>${ev.name}</dt>
    <dd><dl>
      <dt>${le.name}</dt>
      <dd><dl>
        <dt>${te.name}</dt>
        <dd>Members:
          <ul>
          % for me in te.students:
            <li>${me.display_name}</li>
          % endfor
          </ul>
        </dd>
      </dl></dd>
    </dl></dd>
  % endfor
  </dl>

  <h3>Submissions:</h3>
  <ul>
  % for submission in user.submissions:
    <li>${submission.link} for Assignment ${submission.assignment.link}</li>
  % endfor
  </ul>

% endif