<%inherit file="local:templates.master" />
<%namespace file="local:templates.lists" name="lists" />

<%def name="title()">
  News
</%def>

<div class="page-header">
  <h1>News</h1>
</div>

% if news:
  
  ${lists.news(news)}
  
  % if hasattr(tmpl_context, 'paginators') and hasattr(tmpl_context.paginators, 'news'):
    <p>${tmpl_context.paginators.news.pager()}</p>
  % endif
% endif

