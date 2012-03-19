<%inherit file="local:templates.master"/>

<%def name="title()">
  Testruns
</%def>

<h2>Testruns</h2>

% if testruns:
  <table>
  % for testrun in testruns:
    <tr>
      <td>${testrun}</td>
    </tr>
  % endfor
  </table>
% endif
