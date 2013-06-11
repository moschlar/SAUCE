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

<%inherit file="local:templates.master" />

<%def name="title()">
  Similarity ${view}
</%def>

<%def name="headers()">
  <style type="text/css">
    th, td { text-align: center !important; }
  </style>
</%def>

<%def name="th(submission)">
<th class="po" rel="popover" title="Submission ${submission.id}" data-content="<dl>
  <dt>User:</dt><dd>${submission.user}</dd>
  % if submission.team:
    <dt>Team:</dt><dd>${submission.team}</dd>
  % endif
  <dt>Created:</dt><dd>${submission.created.strftime('%c').decode('utf8')}</dd>
  <dt>Last modified:</dt><dd>${submission.modified.strftime('%c').decode('utf8')}</dd>
  </dl>">
  <a href="${submission.url}" style="color: white">
    <span class="badge ${'' if submission.result is None else ('badge-success' if submission.result else 'badge-error')}">
      ${submission.id}
    </span>
  </a>
</th>
</%def>

<div class="page-header">
  <h1>Similarity ${view}
    % if assignment:
      <small>for Assignment: ${assignment.link}</small>
    % endif
  </h1>
</div>

<div class="row">

% if view == 'table':

  <div class="span12">

<table class="table table-condensed table-striped table-bordered similarity">
  <thead>
    <tr>
      <th>&nbsp;</th>
    % for j, s in reversed(list(enumerate(submissions))[1:]):
      ${th(s)}
    % endfor
    </tr>
  </thead>
  <tbody>
  % for i, row in list(enumerate(matrix))[:-1]:
    <tr>
      ${th(submissions[i])}
    % for j, cell in reversed(list(enumerate(row))[1:]):
      % if i >= j:
       <td>&nbsp;</td>
      % else:
        <% sameteam = bool(set(submissions[i].teams) & set(submissions[j].teams)) %>
        <td class="tt" rel="tooltip" title="\
          Submission ${submissions[i].id} and ${submissions[j].id}<br />\
          Distance: ${'%.2f' % cell}\
          ${sameteam and '<br /><i>(Same team)</i>' or ''}">
          <a href="${tg.url(c.url + '/diff/%d/%d/' % (submissions[i].id, submissions[j].id))}"\
            style="color: ${sameteam and '#555555' or c.rgb(cell)}; ${sameteam and 'font-style: italic;' or ''}">
            ${'%.2f' % (1.0 - cell)}
          </a>
        </td>
      % endif
    % endfor
    </tr>
  % endfor
  </tbody>
</table>

  </div>

% elif view == 'list':

  <div class="span6">

<table class="table table-condensed table-striped table-bordered">
  <thead>
    <tr>
      <th colspan="2">Submissions</th>
      <th>Similarity</th>
    </tr>
  </thead>
  <tbody>
  % for (a, b), x in l:
    <tr>
      ${th(a)}
      ${th(b)}
      <% sameteam = bool(set(a.teams) & set(b.teams)) %>
      <td class="tt" rel="tooltip" title="\
        Submission ${a.id} and ${b.id}<br />\
        Distance: ${'%.2f' % x}\
        ${sameteam and '<br /><i>(Same team)</i>' or ''}">
        <a href="${tg.url(c.url + '/diff/%d/%d/' % (a.id, b.id))}"\
          style="color: ${sameteam and '#555555' or c.rgb(x)}; ${sameteam and 'font-style: italic;' or ''}">
            ${'%.2f' % (1.0 - x)}
        </a>
      </td>
    </tr>
    % endfor
  </tbody>
</table>

  </div>

% endif

</div>

<script type="text/javascript">$('.po').popover({placement: 'right', delay: {show: 0, hide: 200}})</script>
<script type="text/javascript">$('.tt').tooltip({placement: 'top'})</script>

<div class="row">
  <div class="span8">
    <ul class="thumbnails">
      <li class="span8">
        <a href="${c.url}/dendrogram.png">
          <div class="thumbnail">
            <img src="${c.url}/dendrogram.png" />
          </div>
        </a>
      </li>
    </ul>
  </div>
  <div class="span4">
    <div class="well" style="margin-top: 45px;">
      <h4>Dendrogram</h4>
      <p>Take a closer look at the submissions which are clustered together
      with small distances and especially those that are nearly at 0.0.</p>
    </div>
  </div>
</div>

