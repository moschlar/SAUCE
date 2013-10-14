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
<%
  try:
    heading = 'Submission %d' % submission.id
  except:
    heading = 'Submission'
  %>
  ${heading}
</%def>

<div class="page-header">
  <h1>${self.title()}
    % if submission.assignment:
      <small>for Assignment: ${submission.assignment.link}</small>
    % endif
  </h1>
</div>

% if getattr(c, 'newer', False):
  <div class="alert alert-info">
  This is not the <abbr title="There are submissions with a later modification time than this one!">newest</abbr>
  submission for this assignment - 
  % if len(c.newer) == 1:
    there is one submission that's
  % else:
    there are ${len(c.newer)} submissions that are
  % endif
    newer:<br />
  % if len(c.newer) == 1:
    It is
  % else:
    The most current one is
  % endif
    <strong>${c.newer[0].link}</strong>
  % if c.newer[0].user != request.user:
    by ${c.newer[0].user}.
  % else:
    by yourself.
  % endif
  </div>
% endif

% if request.allowance(submission) or \
  getattr(request, 'user', None) == submission.user:
  <div class="modal hide fade" id="deleteModal">
    <div class="modal-header">
      <button type="button" class="close" data-dismiss="modal">×</button>
      <h3>Are you sure?</h3>
    </div>
    <div class="modal-body">
      <p>
        This will delete ${submission} from the database.<br />
        You can not revert this step!
      </p>
    </div>
    <div class="modal-footer">
      <a href="#" class="btn" data-dismiss="modal">Cancel</a>
      <a href="${submission.url}/delete" class="btn btn-danger">
        <i class="icon-remove icon-white"></i>&nbsp;Delete&nbsp;${submission}
      </a>
    </div>
  </div>
% endif

<ul class="nav nav-tabs">
  <li class="${('', 'active')['show' in page]}">
    <a href="${submission.url}/show"><i class="icon-eye-open"></i>&nbsp;Show</a>
  </li>

  % if getattr(request, 'user', None) == submission.user and (submission.assignment.is_active or request.allowance(submission)):
    <li class="${('', 'active')['edit' in page]}">
      <a href="${submission.url}/edit"><i class="icon-pencil"></i>&nbsp;Edit</a>
    </li>
  % endif

  <li class="${('', 'active')['result' in page]}">
    <a href="${submission.url}/result"><i class="icon-flag"></i>&nbsp;Result</a>
  </li>

  %if request.allowance(submission):
    <li class="${('', 'active')['judge' in page]}">
      <a href="${submission.url}/judge"><i class="icon-tag"></i>&nbsp;Judge</a>
    </li>
  % endif

  % if request.allowance(submission) or \
    getattr(request, 'user', None) == submission.user:
    % if submission.public:
    <li class="${('', 'active')['public' in page]}">
      <a href="${submission.url}/public/false" title="Submission is currently public. Click to depublicize."><i class="icon-eye-open"></i>&nbsp;Public</a>
    </li>
    % else:
    <li class="${('', 'active')['public' in page]}">
      <a href="${submission.url}/public/true" title="Submission is currently private. Click to publicize."><i class="icon-eye-close"></i>&nbsp;Private</a>
    </li>
    % endif
  % endif

    <li class="${('', 'active')['clone' in page]}">
      <a href="${submission.url}/clone"><i class="icon-retweet"></i>&nbsp;Clone</a>
    </li>

  % if request.allowance(submission) or \
    getattr(request, 'user', None) == submission.user:
    <li class="${('', 'active')['delete' in page]}">
      <a href="#deleteModal" data-toggle="modal" title="Delete">
        <i class="icon-remove"></i>&nbsp;<span style="color:#B94A48;">Delete</span>
      </a>
    </li>
  % endif
</ul>

<dl class="dl-horizontal">
  <dt>User:</dt>
  <dd>${submission.user.display_name}</dd>

  <dt>Created:</dt>
  <dd title="${h.strftime(submission.created, False)}">${h.strftime(submission.created, True)}</dd>
  <dt>Last modified:</dt>
  <dd title="${h.strftime(submission.modified, False)}">${h.strftime(submission.modified, True)}</dd>
</dl>

${next.body()}

<%def name="details(submission)">

<dl class="dl-horizontal">
      <dt>Language:</dt>
      <dd>
        % if submission.language:
          <a href="${tg.url('/languages/%d' % (submission.language.id))}">${submission.language}</a>
        % else:
          None&nbsp;
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
    </p>

  <div>
    ${c.pygmentize.display(id="source_container", lexer_name=submission.language.lexer_name, source=submission.source) | n}
  </div>

  % else:
    <p>No source code submitted yet.</p>
  % endif
  
</%def>

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
    ${c.pygmentize.display(lexer_name=judgement.submission.language.lexer_name, source=judgement.corrected_source) | n}

    <h4>Diff</h4>
    ${c.pygmentize.display(lexer_name='diff', source=judgement.diff) | n}
  % endif

</%def>

<%def name="compilation(compilation)">

  <h3>Compilation result</h3>
  % if compilation.returncode == 0:
    <p>Success</p>
  % else:
    <p>Fail</p>
  % endif
  <table>
  <tr>
    <th>stdout</th><th>stderr</th>
  </tr>
  <tr>
    <td><pre>${compilation.stdout}</pre></td>
    <td><pre>${compilation.stderr}</pre></td>
  </tr>
  </table>

</%def>
