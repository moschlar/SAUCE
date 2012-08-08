<%inherit file="local:templates.master" />

<%def name="title()">
  Similarity table
</%def>

% if assignment:

<div class="page-header">
  <h1>Similarity table <small>Assignment ${assignment.id}</small></h1>
</div>

<div class="row">
<div class="span12">
<h2>${assignment.name}</h2>

<table class="table table-condensed table-striped table-bordered">
<thead>
<tr>
<th>&nbsp;</th>
% for i, row in sorted(matrix.iteritems(), key=lambda s: s[0].id):
<th><a href="${i.url}" title="\
Submission ${i.id}
User: ${i.user}
Created: ${i.created.strftime('%x %X')}
Last modified: ${i.modified.strftime('%x %X')}\
">${i.id}</a>
<span class="badge ${'' if i.result is None else ('badge-success' if i.result else 'badge-error')}">&nbsp;</span>
</th>
% endfor
</tr>
</thead>
<tbody>
% for i, row in sorted(matrix.iteritems(), key=lambda s: s[0].id):
<tr>
<th><a href="${i.url}" title="\
Submission ${i.id}
User: ${i.user}
Created: ${i.created.strftime('%x %X')}
Last modified: ${i.modified.strftime('%x %X')}\
">${i.id}</a>
<span class="badge ${'' if i.result is None else ('badge-success' if i.result else 'badge-error')}">&nbsp;</span>
</th>
% for j, cell in sorted(row.iteritems(), key=lambda s: s[0].id):
<td>
% if i == j:
  &nbsp;
% else:
  <a href="${tg.url('./diff/%d/%d'%(i.id,j.id))}" style="\##cursor: help;
% if cell['ratio'] > 0.88:
  color: red;
% elif cell['ratio'] > 0.66:
  color: rgb(255, 192, 0);
% else:
  color: black;
% endif
" title="\
Real quick ratio: ${'%.2f' % cell['real_quick_ratio']}
Quick ratio: ${'%.2f' % cell['quick_ratio']}
Ratio: ${'%.2f' % cell['ratio']}\
">${'%.2f' % cell['ratio']}</span>
% endif
</td>
% endfor
</tr>
% endfor
</tbody>
</table>

</div>
</div>

% endif
