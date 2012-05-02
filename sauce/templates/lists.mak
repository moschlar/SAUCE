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
      <table style="border: 1px solid black; width:690px; max-width: 690px;">
      <tr>
        <th>Given input</th>
        <td colspan="2"><pre class="code">${testrun.test.input_data}</pre></td>
      </tr>
      <tr>
        <th>Expected vs. <br />observed stdout</th>
        % if hasattr(testrun, 'output_test'):
        <td><pre class="code">${testrun.output_test}</pre></td>
        % else:
        <td><pre class="code">${testrun.test.output_data}</pre></td>
        % endif
        <td><pre class="code">${testrun.output_data}</pre></td>
      </tr>
      <tr>
        <th>Expected vs. <br />observed stdout</th>
        <td colspan="2">${h.highlight(h.udiff(testrun.test.output_data or testrun.output_test, testrun.output_data), 'diff') | n}</td>
      </tr>
      <tr>
        <th>Real stderr</th>
        <td colspan="2"><pre class="code">${testrun.error_data}</pre></td>
      </tr>
    </table>

  % endfor
</%def>