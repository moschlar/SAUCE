<%inherit file="local:templates.master"/>

<%def name="title()">
  Scoreboard
</%def>

<h2>Scoreboard</h2>

% if teams:
  <h3>Teams</h3>
  <table>
    <tr>
     <th>Name</th>
     <th>Correct submissions</th>
     <th>Score</th>
    </tr>
  % for team in teams:
    <tr>
      <td style="font-weight: bold">${team.name}:</td> 
      <td>${team.count}</td>
      <td>${team.score}</td>
    </tr>
  % endfor
  </table>
% endif

% if students:
  <h3>Students</h3>
  <table>
    <tr>
     <th>Name</th>
     <th>Correct submissions</th>
     <th>Score</th>
    </tr>
  % for student in students:
    <tr>
      <td style="font-weight: bold">${student.name}:</td> 
      <td>${student.count}</td>
      <td>${student.score}</td>
    </tr>
  % endfor
  </table>
% endif
