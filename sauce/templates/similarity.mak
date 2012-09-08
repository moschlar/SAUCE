<%inherit file="local:templates.master" />

<%def name="title()">
  Similarity table
</%def>

<%def name="th(submission)">
<th class="po" rel="popover" title="Submission ${submission.id}" data-content="<dl>\
<dt>User:</dt><dd>${submission.user}</dd>\
<dt>Created:</dt><dd>${submission.created.strftime('%x %X')}</dd>\
<dt>Last modified:</dt><dd>${submission.modified.strftime('%x %X')}</dd>\
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
  <td class="tt" rel="tooltip" title="Distance: ${'%.2f' % cell}">
    <a href="${tg.url(c.url + '/diff/%d/%d/' % (submissions[i].id, submissions[j].id))}" style="color: ${c.rgb(cell)};">${'%.2f' % (1.0 - cell)}</a>
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

<img src="${c.url}/dendrogram.png" />

</div>
</div>


