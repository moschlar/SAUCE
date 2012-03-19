<%inherit file="local:templates.master"/>

<%def name="title()">
  Scores
</%def>

<h2>Scores</h2>

% if students:
  <table>
  % for student in students:
    <tr>
      <td style="font-weight: bold">${student.name}:</td> 
      <td>${student.score}</td>
    </tr>
  % endfor
  </table>
% endif
