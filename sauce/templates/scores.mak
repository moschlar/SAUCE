## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
         ${a.link}
         (${a.solution[team.id].language.name}, ${'%.3f sec' % a.solution[team.id].testrun.runtime})<br />
       % endfor
      </td>
    </tr>
  % endfor
  </table>
% endif
