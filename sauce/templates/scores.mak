<%inherit file="local:templates.master"/>

<%def name="title()">
  Scoreboard
</%def>

<h2>Scoreboard</h2>

<p class="red">Currently broken</p>

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
