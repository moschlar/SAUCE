<%inherit file="local:templates.master"/>

% if event:
<%def name="body_class()">navbar_left</%def>
% endif


<%def name="title()">
  Submission
</%def>

<h2>Submission 
% if submission and hasattr(submission, 'id'):
  ${submission.id}
% endif
</h2>

<p>
% if assignment:
for Assignment: ${h.link(assignment.name, tg.url('/assignments/%d' % assignment.id))}
% endif
</p>


% if not submission.complete:
  ${c.form(c.options, child_args=c.child_args) | n}
% else:
  <div>
  <table>
    <tr>
      <th>Result</th>
      <td>
        % if submission.result:
          <span class="green">ok</span>
        % else:
          <span class="red">fail</span>
        % endif
      </td>
    </tr>
    <tr>
      <th>Language</th>
      <td>${submission.language}</td>
    </tr>
    <tr>
      <th>Runtime</th>
      <td>${submission.runtime}</td>
    </tr>
  </table>
   
  <h3>Source code</h3>
  <pre id="src" class="brush: ${submission.language.brush};">${submission.source}</pre>

% if submission.judgement:

  % if submission.judgement.annotations:
  <h4>Annotations:</h4>
    <table>
    % for line, ann in submission.judgement.annotations.iteritems():
      <tr>
        <th>
          <a href="javascript:highline(${line})">Line ${line}</a>
        </th>
        <td>
          ${ann}
        </td>
      </tr>
    % endfor
    </table>
  % endif

% endif

% endif

% if compilation:
  <h3>Compilation result</h3>
  % if compilation.returncode == 0:
    <p>Success</p>
  % else:
    <p>Fail</p>
  % endif
  <table>
  <tr>
    <th>stdout</th><th>stderr</th>
  </tr>
  <tr>
    <td><pre>${compilation.stdout}</pre></td>
    <td><pre>${compilation.stderr}</pre></td>
  </tr>
  </table>
% endif

% if testruns:
  <h3>Testrun results</h3>
  % for testrun in testruns:
    % if testrun.result:
      <p>Success</p>
    % else:
      <p>Fail</p>
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
        <td><pre>${testrun.test.output_data}</pre></td>
        <td><pre>${testrun.process.stdout}</pre></td>
        <td><pre>${testrun.process.stderr}</pre></td>
      </tr>
    </table>
  % endfor
% endif

<p>
<a href="javascript:highline(2);">2</a>
<a href="javascript:highline(3);">3</a>
</p>

% if submission.language and submission.language.brush:
    <script type="text/javascript" src="/sh/scripts/shCore.js"></script>
    <script type="text/javascript" src="/sh/scripts/shBrush${submission.language.brush.capitalize()}.js"></script>
    <link type="text/css" rel="stylesheet" href="/sh/styles/shCoreDefault.css"/>
    <script type="text/javascript">
<%doc>
      function linecount() {
    	  /* Surrounding div */
    	  var obj = document.getElementById('src');
    	  /* highlighter div */
    	  obj = obj.childNodes[0];
    	  /* table */
    	  obj = obj.childNodes[0];
    	  /* tbody */ 
    	  obj = obj.childNodes[0];
    	  /* tr */
    	  obj = obj.childNodes[0];
    	  /* gutter */
    	  obj = obj.childNodes[0];
    	  return obj.childElementCount;
      }
</%doc>
       function highline(number) {
    	  var high = document.getElementsByClassName("highlighted");
    	  for (var i=0; i < high.length; ++i) {
    		  high[i].classList.remove("highlighted");
    	  }
          var line = document.getElementsByClassName("number"+number);
          for (var j=0; j < line.length; ++j) {
              line[j].classList.add("highlighted");
          }
      }
      SyntaxHighlighter.defaults['auto-links'] = false; 
      SyntaxHighlighter.defaults['toolbar'] = false; 
      SyntaxHighlighter.all();
    </script>
% endif