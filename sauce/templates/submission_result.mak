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

<%inherit file="local:templates.submission" />

<%def name="headers()">
  <style type="text/css">
${h.style}
  </style>
</%def>

<div class="pull-right">
  <a href="${tg.url(submission.url + '/result', dict(force_test=1))}" class="btn">
    <i class="icon-repeat"></i>&nbsp;Run tests again
  </a>
</div>

% if compilation:
  <h2>Compilation result</h2>
  % if compilation.result:
    <p class="label label-success">Success</p>
  % else:
    <p class="label label-important">Fail</p>
  % endif
    <table class="table table-bordered">
      <tr>
        <th>Runtime</th>
        <td>${compilation.runtime} seconds</td>
      </tr>
    % if compilation.stdout:
      <tr>
        <th>stdout</th>
        <td><pre>${compilation.stdout}</pre></td>
      </tr>
    % endif
    % if compilation.stderr:
      <tr>
        <th>stderr</th>
        <td><pre>${compilation.stderr}</pre></td>
      </tr>
    % endif
    </table>
% endif

% if testruns:
  <h2>Testrun results</h2>
  ${self.list(testruns)}
% endif

<%def name="list(testruns)">
  % for testrun in testruns:
  % if testrun.test.visible or request.allowance(testrun):
    % if request.allowance(testrun):
      <div class="row"><div class="span6">
    % endif
    % if testrun.result:
      <p class="label label-success" title="Your submission is correct. Congratulations!">
        Success
      </p>
    % else:
      % if testrun.partial:
        <p class="label label-warning" title="Your submission is partially correct.
Check the output below and compare it to the expected output.
Check your program for missing characters or a probable infinite loop.">
           Partial match
         </p>
      % else:
        <p class="label label-important" title="Your submission is producing wrong or no output.
Check the output and error listing below to see what went wrong.">
          Fail
        </p>
      % endif
    % endif
    % if request.allowance(testrun):
      </div><div class="span6">
      % if testrun.test.visible:
        <p class="label"><i class="icon-eye-open icon-white"></i>&nbsp;Visible test</p>
      % else:
        <p class="label label-inverse"><i class="icon-eye-close icon-white"></i>&nbsp;Invisible test</p>
      % endif
      </div></div>
    % endif
      <table class="table table-bordered">
      <tr>
        <th>Date</th>
        <td colspan="2">${testrun.date.strftime('%c')}</td>
      </tr>
      <tr>
        <th>Runtime</th>
        <td colspan="2">${testrun.runtime} seconds</td>
      </tr>
% if testrun.test.input_data:
      <tr>
        <th>Given input</th>
        <td colspan="2"><pre>${testrun.test.input_data}</pre></td>
      </tr>
% endif
% if testrun.result:
      <tr>
        <th>Expected and<br />observed output</th>
        <td colspan="2"><pre>${testrun.output_data}</pre></td>
      </tr>
% else:
      <tr>
        <th>Expected vs.<br />observed output</th>
        <td><pre>${testrun.test.test_output_data}</pre></td>
        <td><pre>${testrun.output_data}</pre></td>
      </tr>
      <tr>
        <th>Expected vs. <br />observed stdout<br />(<a href="http://en.wikipedia.org/wiki/Diff#Unified_format">diff</a>)</th>
        <td colspan="2">${h.highlight(h.udiff(testrun.test.test_output_data, testrun.output_data, 'expected', 'observed'), 'diff') | n}</td>
      </tr>
% endif
% if testrun.error_data:
      <tr>
        <th>Error message(s)</th>
        <td colspan="2"><pre>${testrun.error_data}</pre></td>
      </tr>
% endif
    </table>
  % endif
  % endfor
</%def>
