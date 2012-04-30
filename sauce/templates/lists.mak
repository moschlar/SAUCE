<%namespace file="local:templates.misc" import="times_dl" />

<%!
  import string
  import sauce.lib.helpers as h
%>

<%def name="events(events)">

<dl>
  % for event in events:
##    <dt>${h.link(event.name, tg.url('/events/%s' % event.url))} (${event.type | string.capitalize})</dt>
    <dt>${event.link} (${event.type | string.capitalize})</dt>
    <dd>${event.description | n, h.striphtml, h.cut }</dd>
  % endfor
</dl>

</%def>

<%def name="assignments(assignments)">

<dl>
  %for assignment in assignments:
    <dt>${assignment.link}</dt>
    
    <dd>${assignment.description | n, h.striphtml, h.cut }</dd>
  %endfor
</dl>

</%def>

<%def name="sheets_short(sheets)">

<dl>
  % for sheet in sheets:
    <dt>${sheet.link}</dt>
    <dd>
      <p>${sheet.description | n, h.striphtml, h.cut }</p>
    </dd>
  % endfor
</dl>

</%def>

<%def name="sheets(sheets)">

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
      ${assignments(sheet.assignments)}</p>
    </dd>
  % endfor
</dl>

</%def>

<%def name="news(news)">
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

<%def name="testruns(testruns)">
  <h3>Testrun results</h3>
  % for testrun in testruns:
    % if testrun.result:
      <p class="green">Success</p>
    % else:
      <p class="red">Fail</p>
    % endif
      <table>
      <tr>
        <th>Given input</th>
        <th>Expected stdout</th>
        <th>Real stdout</th>
        <th>Real stderr</th>
      </tr>
      <tr>
        <td><pre>${testrun.test.input_data}</pre></td>
        % if hasattr(testrun, 'output_test'):
        <td><pre>${testrun.output_test}</pre></td>
        % else:
        <td><pre>${testrun.test.output_data}</pre></td>
        % endif
        <td><pre>${testrun.output_data}</pre></td>
        <td><pre>${testrun.error_data}</pre></td>
      </tr>
    </table>

  % endfor
</%def>