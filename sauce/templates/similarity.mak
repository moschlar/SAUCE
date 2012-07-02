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

<div>
<table class="well">
<tr>
<th>&nbsp;</th>
% for i, row in sorted(matrix.iteritems(), key=lambda s: s[0].id):
<th>${i.id}</th>
% endfor
</tr>
% for i, row in sorted(matrix.iteritems(), key=lambda s: s[0].id):
<tr>
<th>${i.id}</th>
% for j, cell in sorted(row.iteritems(), key=lambda s: s[0].id):
<td>
% if i == j:
  &nbsp;
% else:
  <a href="${tg.url('/diff/%d/%d'%(i.id,j.id))}" style="cursor: help;
% if cell['ratio'] > 0.88:
  color: red;
% elif cell['ratio'] > 0.66:
  color: rgb(255, 192, 0);
% endif
"
title="Real quick ratio: ${'%.2f' % cell['real_quick_ratio']}
Quick ratio: ${'%.2f' % cell['quick_ratio']}
Ratio: ${'%.2f' % cell['ratio']}">
  ${'%.2f' % cell['ratio']}</span>
% endif
</td>
% endfor
</tr>
% endfor
</table>
</div>

</div>
</div>

% endif
