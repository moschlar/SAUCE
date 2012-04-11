<%inherit file="local:templates.master"/>
<%namespace file="local:templates.lists" name="lists" />

<%def name="title()">
  News
</%def>

<h2>News</h2>

% if news:
  
  ${lists.news(news)}
  
  % if hasattr(news, 'pager'):
    <p>${news.pager('Pages: $link_previous ~2~ $link_next')}</p>
  % endif
% endif

