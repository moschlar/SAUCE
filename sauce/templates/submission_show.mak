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

<%inherit file="local:templates.submission_details" />

% if submission.judgement:
  <h2>Judgement</h2>
  ${details_judgement(submission.judgement)}
% endif

<%def name="details_judgement(judgement)">

  % if judgement.annotations:
    <h3>Annotations:</h3>
      <dl class="dl-horizontal">
      % for line, ann in sorted(judgement.annotations.iteritems()):
        <dt>
          <a href="javascript:highline('source_container', 'line-${line}')">Line ${line}</a>
        </dt>
        <dd>
          ${ann}
        </dd>
      % endfor
      </dl>
    % endif

  % if judgement.comment:
    <h3>Comment:</h3>
    <p>${judgement.comment | n}</p>
  % endif

  % if judgement.corrected_source:
    <h3>Corrected source code:</h3>
    <p class="btn-group">
      <a href="${judgement.submission.url}/source/judgement" class="btn btn-mini"><i class="icon-file"></i>&nbsp;Full page</a>
      <a href="${judgement.submission.url}/download/judgement" class="btn btn-mini"><i class="icon-download-alt"></i>&nbsp;Download</a>
    </p>
    ${c.pygmentize.display(source=judgement.corrected_source) | n}

    <h4>Diff</h4>
    ${c.pygmentize.display(lexer_name='diff', source=judgement.diff) | n}
  % endif

</%def>
