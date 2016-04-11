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
    <table class="table table-bordered table-condensed test-and-result-table">
      <tr>
        <th>Runtime</th>
        <td>${compilation.runtime} seconds</td>
      </tr>
    % if submission.assignment.show_compiler_msg:
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
    % endif
    </table>
% endif

% if testruns:
  <h2>Testrun results</h2>
  ${self.list(testruns)}
% endif

<%def name="list(testruns)">
  % for testrun in testruns:
    % if testrun.test.visibility != 'invisible' or request.allowance(testrun):
      <table class="table table-bordered table-condensed test-and-result-table">
      % if request.allowance(testrun):
        <tr>
          <th>Test</th>
          <th>${testrun.test.name}</th>
          <th>
          % if testrun.test.visibility == 'visible':
            <span class="label"><i class="icon-eye-open icon-white"></i>&nbsp;Visible</span>
          % elif testrun.test.visibility == 'result_only':
            <span class="label"><i class="icon-eye-close icon-white"></i>&nbsp;Only result visible</span>
          % elif testrun.test.visibility == 'data_only':
            <span class="label"><i class="icon-eye-close icon-white"></i>&nbsp;Only data visible</span>
          % elif testrun.test.visibility == 'invisible':
            <span class="label label-inverse"><i class="icon-eye-close icon-white"></i>&nbsp;Invisible</span>
          % endif
          </th>
        </tr>
      % endif
      <tr>
        <th>Date</th>
        <td colspan="2"><span title="${h.strftime(testrun.date, False)}">${h.strftime(testrun.date, True)}</td>
      </tr>
      <tr>
        <th>Runtime</th>
        <td colspan="2">${testrun.runtime} seconds</td>
      </tr>
      % if testrun.test.visibility in ('visible', 'result_only') or request.allowance(testrun):
        <tr>
          <th>Result</th>
          <td colspan="2">
          % if testrun.result:
            <span class="label label-success" title="Your submission is correct. Congratulations!">
              Success
            </span>
          % else:
            % if testrun.partial:
              <span class="label label-warning" title="Your submission is partially correct.
  Check the output below and compare it to the expected output.
  Check your program for missing characters or a probable infinite loop.">
                 Partial match
               </span>
            % else:
              <span class="label label-important" title="Your submission is producing wrong or no output.
  Check the output and error listing below to see what went wrong.">
                Fail
              </span>
            % endif
          % endif
          </td>
        </tr>
      % endif
      % if testrun.test.visibility in ('visible', 'data_only') or request.allowance(testrun):
        % if testrun.test.argv:
          <tr>
            <th>Command line arguments</th>
            <td colspan="2"><pre>${testrun.test.argv}</pre></td>
          </tr>
        % endif
        % if testrun.test.visibility == 'data_only':
            <tr>
              <th>Observed output</th>
              <td colspan="2"><pre>${testrun.output_data}</pre></td>
            </tr>
        % else:
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
              <td><pre>${testrun.test.output_data}</pre></td>
              <td><pre>${testrun.output_data}</pre></td>
            </tr>
            % if len(testrun.output_data) < 65536:
            <tr>
              <th>
              Expected vs.<br />observed output<br />
              <em>
                (<a href="http://en.wikipedia.org/wiki/Diff#Unified_format">Unified diff format</a>)
              </em>
              </th>
              <td colspan="2">
                ${c.source_display.display(h.udiff(testrun.test.output_data, testrun.output_data, 'expected', 'observed'),
                  id='diff_%d' % loop.index, compound_id='diff_%d' % loop.index,
                  mode='diff', lineNumbers=False) | n}
                % if testrun.test.comment_prefix:
                  <em>(Highlighted lines that start with the test comment prefix <code>${testrun.test.comment_prefix}</code>
                  are not relevant for the result!)</em>
                % endif
              </td>
            </tr>
            % endif
          % endif
        % endif
        % if testrun.error_data:
          <tr>
            <th>Error message(s)</th>
            <td colspan="2"><pre>${testrun.error_data}</pre></td>
          </tr>
        % endif
      % endif
      </table>
    % endif
  % endfor
</%def>
