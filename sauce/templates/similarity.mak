<%inherit file="local:templates.master" />

<%def name="title()">
  Similarity table
</%def>

<%def name="th(submission)">
<th class="po" rel="popover" title="Submission ${submission.id}" data-content="<dl>
<dt>User:</dt><dd>${submission.user}</dd>
% if submission.team:
  <dt>Team:</dt><dd>${submission.team}</dd>
% endif
<dt>Created:</dt><dd>${submission.created.strftime('%c')}</dd>
<dt>Last modified:</dt><dd>${submission.modified.strftime('%c')}</dd>
</dl>">
<span class="badge ${'' if submission.result is None else ('badge-success' if submission.result else 'badge-error')}">
<a href="${submission.url}" style="color: white">${submission.id}</a>
</span>
</th>
</%def>


<div class="page-header">
  <h1>${assignment.name} <small>Similarity table</small></h1>
</div>


<div class="row">
<div class="span12">

<table class="table table-condensed table-striped table-bordered similarity">
<thead>
<tr>
<th>&nbsp;</th>
% for j, s in enumerate(submissions):
${th(s)}
% endfor
<th>&nbsp;</th>
</tr>
</thead>
<tbody>
% for i, row in enumerate(matrix):
<tr>
${th(submissions[i])}
% for j, cell in enumerate(row):
% if i == j:
  <td>&nbsp;</td>
% else:
<% sameteam = bool(set(submissions[i].teams) & set(submissions[j].teams)) %>
  <td class="tt" rel="tooltip" title="${sameteam and 'Same team<br />' or ''}Distance: ${'%.2f' % cell}">
    <a href="${tg.url(c.url + '/diff/%d/%d/' % (submissions[i].id, submissions[j].id))}"\
      style="color: ${sameteam and '#555555' or c.rgb(cell)}; ${sameteam and 'font-style: italic;' or ''}">
        ${'%.2f' % (1.0 - cell)}
    </a>
  </td>
% endif
% endfor
${th(submissions[i])}
</tr>
% endfor
</tbody>
<tfoot>
<tr>
<th>&nbsp;</th>
% for j, s in enumerate(submissions):
${th(s)}
% endfor
<th>&nbsp;</th>
</tr>
</tfoot>
</table>

<script type="text/javascript">$('.po').popover({placement: 'right', delay: {show: 0, hide: 200}})</script>
<script type="text/javascript">$('.tt').tooltip({placement: 'top'})</script>

</div>
</div>
<div class="row">
  <div class="span8">
    <ul class="thumbnails">
      <li class="span8">
        <div class="thumbnail">
          <img src="${c.url}/dendrogram.png" />
        </div>
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

