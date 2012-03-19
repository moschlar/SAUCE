<%inherit file="local:templates.master"/>

<%def name="title()">
  Testruns
</%def>

<h2>Testruns</h2>

% if testruns:
  <table>
    <tr>
      <th>Date</th>
      <th>Result</th>
  % for testrun in testruns:
    <tr>
      <td>${testrun.date}</td>
      <td>${testrun.result}</td>
    </tr>
  % endfor
  </table>
% endif
