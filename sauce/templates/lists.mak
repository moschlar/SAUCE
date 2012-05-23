<%namespace file="local:templates.misc" import="times_dl" />

<%!
  import string
  import sauce.lib.helpers as h
%>

<%def name="testruns(testruns)">
  <h3>Testrun results</h3>
  % for testrun in testruns:
    % if testrun.result:
      <p class="label label-success">Success</p>
    % else:
      <p class="label label-important">Fail</p>
    % endif
      <table style="border: 1px solid black; width:690px; max-width: 690px;">
% if testrun.test.input_data:
      <tr>
        <th>Given input</th>
        <td colspan="2"><pre>${testrun.test.input_data}</pre></td>
      </tr>
% endif
      <tr>
        <th>Expected vs. <br />observed stdout</th>
        <td><pre>${testrun.test.test_output_data}</pre></td>
        <td><pre>${testrun.output_data}</pre></td>
      </tr>
% if not testrun.result:
      <tr>
        <th>Expected vs. <br />observed stdout<br />(<a href="http://en.wikipedia.org/wiki/Diff#Unified_format">diff</a>)</th>
        <td colspan="2">${h.highlight(h.udiff(testrun.test.test_output_data, testrun.output_data, 'expected', 'observed'), 'diff') | n}</td>
      </tr>
% endif
% if testrun.error_data:
      <tr>
        <th>Observed stderr</th>
        <td colspan="2"><pre>${testrun.error_data}</pre></td>
      </tr>
% endif
    </table>

  % endfor
</%def>