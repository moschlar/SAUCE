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

% if submissions:
  <h3>Your submissions:</h3>
  <ul>
  % for submission in submissions:
    <li>${submission.link} for Assignment ${submission.assignment.link}</li>
  % endfor
  </ul>
% endif

% if student:

  <h3>Your events:</h3>
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
  
% elif teacher:

  % if teacher['events']:
    <h3>Your events:</h3>
    <ul>
    % for event in teacher['events']:
      <li>${event.link}</li>
    % endfor
    </ul>
  % endif
  % if teacher['lessons']:
    <h3>Your lessons:</h3>
    <ul>
    % for lesson in teacher['lessons']:
      <li>${lesson.link} (${lesson.event.link})</li>
    % endfor
  % endif
  </ul>
<h4>Submissions in your lessons:</h4>
%if teacher['submission_table'] and teacher['submission_values']:
  ${teacher['submission_table'](value=teacher['submission_values']) | n}
%endif
% endif
