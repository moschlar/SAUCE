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

<dl class="dl-horizontal">
  <dt>Language:</dt>
  <dd>
  % if submission.language:
    <a href="${tg.url('/languages/%d' % (submission.language.id))}" target="_blank">${submission.language.name}</a>
  % else:
    None
  % endif
  </dd>

  % if submission.result is not None:
    <dt>Test result:</dt>
    <dd>
    % if submission.result:
      <span class="label label-success">Success</span>
    % else:
     <span class="label label-important">Failed</span>
    % endif
    </dd>
  % endif

  % if submission.judgement:
    <dt>Tutor:</dt>
        <dd>${submission.judgement.tutor.display_name}</dd>
    <dt>Judgement date:</dt>
        <dd title="${h.strftime(submission.judgement.date, False)}">${h.strftime(submission.judgement.date, True)}</dd>
    % if submission.judgement.grade is not None:
      <dt>Grade:</dt>
          <dd><span class="badge badge-info">${submission.judgement.grade}</span></dd>
    % endif
  % endif
</dl>

  <h2>Source code:</h2>
  % if submission.source:
    <p class="btn-group">
      <a href="${submission.url}/source" class="btn btn-mini"><i class="icon-file"></i>&nbsp;Full page</a>
      <a href="${submission.url}/download" class="btn btn-mini"><i class="icon-download-alt"></i>&nbsp;Download</a>
      ##TODO: Download full source button
    </p>
    <div>
      ${c.pygmentize.display(id="source_container", source=submission.source) | n}
    </div>
  % else:
    <p>No source code submitted yet.</p>
  % endif

${next.body()}
