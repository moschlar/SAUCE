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
  <dd title="${submission.user.user_name}">${submission.user.display_name}</dd>

  <dt>Created:</dt>
  <dd title="${h.strftime(submission.created, False)}">${h.strftime(submission.created, True)}</dd>
  <dt>Last modified:</dt>
  <dd title="${h.strftime(submission.modified, False)}">${h.strftime(submission.modified, True)}</dd>

  <dt>Publicity:</dt>
  <dd>
    <div class="btn-group">
      <a href="#" class="btn btn-mini disabled"  title="Submission is currently ${('private', 'public')[submission.public]}.">
        ${('Private', 'Public')[submission.public]}
      </a>
  % if request.allowance(submission) or \
      getattr(request, 'user', None) == submission.user:
        <a href="${submission.url}/public/false" class="btn btn-mini ${('active', '')[submission.public]}" title="Click to make private.">
          <i class="icon-eye-close">&nbsp;</i>
        </a>
        <a href="${submission.url}/public/true" class="btn btn-mini ${('', 'active')[submission.public]}" title="Click to make public.">
          <i class="icon-eye-open">&nbsp;</i>
        </a>
  % endif
    </div>
  </dd>

</dl>

${next.body()}
