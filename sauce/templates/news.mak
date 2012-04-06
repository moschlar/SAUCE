<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" import="news_list" />

<%def name="title()">
  News
</%def>

<h2>News</h2>

% if news:
  
  ${news_list(news)}
  
  % if hasattr(news, 'pager'):
    <p>${news.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

