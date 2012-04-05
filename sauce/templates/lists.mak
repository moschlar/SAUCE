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
    <dt>${h.link(assignment.name, tg.url('/events/%s/sheets/%d/assignments/%d' % (assignment.sheet.event.url, assignment.sheet.sheet_id, assignment.assignment_id)))}</dt>
    
    <dd>${assignment.description | n, h.striphtml, h.cut }</dd>
  %endfor
</dl>

</%def>

<%def name="sheet_list_short(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${h.link(sheet.name, tg.url('/events/%s/sheets/%d' % (sheet.event.url, sheet.sheet_id)))}</dt>
    <dd>
      <p>${sheet.description | n, h.striphtml, h.cut }</p>
    </dd>
  % endfor
</dl>

</%def>

<%def name="sheet_list(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${h.link(sheet.name, tg.url('/events/%s/sheets/%d' % (sheet.event.url, sheet.sheet_id)))}</dt>
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