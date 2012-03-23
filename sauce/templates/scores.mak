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
     <th>Finished assignments</th>
    </tr>
  % for team in teams:
    <tr>
      <td style="font-weight: bold">${team.name}:</td> 
      <td>${team.count}</td>
      <td>${team.score}</td>
      <td>
       % for a in team.assignments:
         ${h.link(a.name, tg.url('/assignments/%d' % a.id))} 
         (${a.solution.language.name}, ${'%.3f sec' % a.solution.testrun.runtime})<br />
       % endfor
      </td>
    </tr>
  % endfor
  </table>
% endif
