<%inherit file="local:templates.master"/>

<%def name="title()">
  News
</%def>

<h2>News</h2>

% if news:
##  <h3>News</h3>
  
  % for newsitem in news.items:
  <div>
    <div style="border: 1px solid black; font-size: 14pt;">${newsitem.subject} - ${newsitem.date.strftime('%x %X')}</div>
    % if newsitem.event:
      <div style="font-style: italic;">For event: ${h.link(newsitem.event.name, tg.url('/events/%d' % newsitem.event.id))}</div>
    % endif
    <p>${newsitem.message | n}</p>
  </div>
  % endfor
  
  <p>${news.pager('Pages: $link_previous ~2~ $link_next')}</p>
 % endif

