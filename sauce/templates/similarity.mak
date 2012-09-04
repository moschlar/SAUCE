<%inherit file="local:templates.master" />

<%def name="title()">
  Similarity table
</%def>

% if assignment:

<div class="page-header">
  <h1>Similarity table <small>Assignment ${assignment.id}</small></h1>
</div>

% if hasattr(c, 'backlink') and c.backlink:
  <div class="span2 pull-right">
    <a href="${c.backlink}" class="btn btn-inverse pull-right">
      <i class="icon-arrow-left icon-white"></i>&nbsp;Go back</a>
  </div>
% endif


<div class="row">
<div class="span12">
<h2>${assignment.name}</h2>

<table class="table table-condensed table-striped table-bordered">
<thead>
<tr>
<th>&nbsp;</th>
% for i, row in sorted(matrix.iteritems(), key=lambda s: s[0].id):
<th><a href="${i.url}" class="po" rel="popover" title="Submission ${i.id}" data-content="<dl>\
<dt>User:</dt><dd>${i.user}</dd>\
<dt>Created:</dt><dd>${i.created.strftime('%x %X')}</dd>\
<dt>Last modified:</dt><dd>${i.modified.strftime('%x %X')}</dd>\
</dl>">${i.id}
<span class="badge ${'' if i.result is None else ('badge-success' if i.result else 'badge-error')}">&nbsp;</span>
</a></th>
% endfor
</tr>
</thead>
<tbody>
% for i, row in sorted(matrix.iteritems(), key=lambda s: s[0].id):
<tr>
<th><a href="${i.url}" class="po" rel="popover" title="Submission ${i.id}" data-content="<dl>\
<dt>User:</dt><dd>${i.user}</dd>\
<dt>Created:</dt><dd>${i.created.strftime('%x %X')}</dd>\
<dt>Last modified:</dt><dd>${i.modified.strftime('%x %X')}</dd>\
</dl>">${i.id}
<span class="badge ${'' if i.result is None else ('badge-success' if i.result else 'badge-error')}">&nbsp;</span>
</a></th>
% for j, cell in sorted(row.iteritems(), key=lambda s: s[0].id):
<td>
% if i == j:
  &nbsp;
% else:
  <a href="${tg.url('./diff/%d/%d'%(i.id,j.id))}" class="tt" style="\##cursor: help;
% if cell['ratio'] > 0.88:
  color: red;
% elif cell['ratio'] > 0.66:
  color: rgb(255, 192, 0);
% else:
  color: black;
% endif
" rel="tooltip" title="\
Real quick ratio: ${'%.2f' % cell['real_quick_ratio']}<br />
Quick ratio: ${'%.2f' % cell['quick_ratio']}<br />
Ratio: ${'%.2f' % cell['ratio']}\
">${'%.2f' % cell['ratio']}</span>
% endif
</td>
% endfor
</tr>
% endfor
</tbody>
</table>
<script type="text/javascript">$('.po').popover({placement: 'right', delay: {show: 0, hide: 200}})</script>
<script type="text/javascript">$('.tt').tooltip({placement: 'top'})</script>

</div>
</div>

%else:

% if hasattr(c, 'backlink') and c.backlink:
  <div class="span2 pull-right">
    <a href="${c.backlink}" class="btn btn-inverse">'
      <i class="icon-arrow-left icon-white"></i>&nbsp;Go back</a>
  </div>
% endif

% endif
