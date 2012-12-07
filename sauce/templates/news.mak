<%inherit file="local:templates.master" />

<%def name="title()">
  News
</%def>

<div class="page-header">
  <h1>News</h1>
</div>

% if news:
  
  ${list(news)}
  
  % if hasattr(tmpl_context, 'paginators') and hasattr(tmpl_context.paginators, 'news'):
    <p>${tmpl_context.paginators.news.pager()}</p>
  % endif
% endif

<%def name="list(news)">
  <dl>
  % for newsitem in news:
    <dt>${newsitem.subject}
      % if not newsitem.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    <dd>
      <em>Posted by ${newsitem.user.link} - ${newsitem.date.strftime('%c')}</em>
      <p>${newsitem.message | n}</p>
    </dd>
  % endfor
  </dl>
</%def>

