<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists"/>

##% if event:
##  <%def name="body_class()">class="navbar_left"</%def>
##% endif

<%def name="title()">
  ${user}
</%def>

<h2>User: ${user}</h2>

<p><a href="${tg.url('/user/profile')}">Edit profile</a></p>

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
% elif teacher:
  % if teacher['events']:
    <h3>Events:</h3>
    <ul>
    % for event in teacher['events']:
      <li>${event.link}</li>
    % endfor
    </ul>
  % endif
  % if teacher['lessons']:
    <h3>Lessons:</h3>
    <ul>
    % for lesson in teacher['lessons']:
      <li>${lesson.link} (${lesson.event.link})</li>
    % endfor
  % endif
  </ul>
% endif
