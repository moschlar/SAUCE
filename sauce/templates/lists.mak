<%namespace file="local:templates.misc" import="times_dl" />

<%!
  import string
  import sauce.lib.helpers as h
%>

<%def name="event_list(events)">

<dl>
  % for event in events:
##    <dt>${h.link(event.name, tg.url('/events/%s' % event.url))} (${event.type | string.capitalize})</dt>
    <dt>${event.link} (${event.type | string.capitalize})</dt>
    <dd>${event.description | n, h.striphtml, h.cut }</dd>
  % endfor
</dl>

</%def>

<%def name="news_list(news)">

<dl>
  % for newsitem in event.news:
    <dt>${newsitem.subject}</dt>
    <dd>
      <p>${newsitem.teacher.name} - ${newsitem.date.strftime('%x %X')}
      <p>${newsitem.message | n }</p>
    </dd>
  % endfor
</dl>

</%def>

<%def name="assignment_list(assignments)">

<dl>
  %for assignment in assignments:
    <dt>${assignment.link}</dt>
    
    <dd>${assignment.description | n, h.striphtml, h.cut }</dd>
  %endfor
</dl>

</%def>

<%def name="sheet_list_short(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${sheet.link}</dt>
    <dd>
      <p>${sheet.description | n, h.striphtml, h.cut }</p>
    </dd>
  % endfor
</dl>

</%def>

<%def name="sheet_list(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${sheet.link}</dt>
    <dd>
      <p>${sheet.description | n, h.striphtml, h.cut }</p>
      ${times_dl(sheet)}
      
##      % if sheet.grade:
##      <dl><dt>Grade:</dt><dd>${sheet.grade}</dd></dl>
##      % endif
      
      <p><strong>Assignments:</strong>
      ${assignment_list(sheet.assignments)}</p>
    </dd>
  % endfor
</dl>

</%def>

<%def name="news_list(news)">
  <dl>
  % for newsitem in news:
    <dt>${newsitem.subject} - ${newsitem.date.strftime('%x %X')}</dt>
    <dd>
    % if newsitem.event:
      <p style="font-style: italic;">For event: ${newsitem.event.link}</p>
    % endif
    <p>${newsitem.message | n}</p>
    </dd>
  % endfor
  </dl>
</%def>