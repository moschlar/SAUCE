<%inherit file="local:templates.master"/>

<%def name="title()">
<%
  try:
    heading = 'Submission %d' % submission.id
  except:
    heading = 'Submission'
  %>
  ${heading}
</%def>

<div class="page-header">
  <h1>${self.title()}
    % if submission.assignment:
      <small>for Assignment: ${submission.assignment.link}</small>
    % endif
  </h1>
</div>

<ul class="nav nav-tabs">
  <li class="${('', 'active')['show' in page]}">
    <a href="${submission.url}/show"><i class="icon-eye-open"></i> Show</a>
  </li>
  <li class="${('', 'active')['edit' in page]}">
    <a href="${submission.url}/edit"><i class="icon-pencil"></i> Edit</a>
  </li>
  %if hasattr(request, 'teacher') and request.teacher:
    <li class="${('', 'active')['judge' in page]}">
      <a href="${submission.url}/judge"><i class="icon-tag"></i> Judge</a>
    </li>
  % endif
</ul>

${next.body()}

<%def name="details(submission)">

<p>Created: ${submission.created.strftime('%x %X')}, Last modified: ${submission.modified.strftime('%x %X')}</p>

  % if not submission.complete and submission.assignment.is_active:
    <p><a href="${tg.url('/submissions/%d/edit' % submission.id)}" class="btn btn-primary">
      Edit submission</a></p>
  % endif

  <table>
    % if len(submission.assignment.allowed_languages) > 1:
      <tr>
        <th>Language</th>
        <td>${submission.language}</td>
      </tr>
    % endif

    % if submission.complete:
      <tr>
        <th>Test result</th>
        <td>
          % if submission.result:
            <span class="label label-success">ok</span>
          % else:
            <span class="label label-important">fail</span>
          % endif
        </td>
      </tr>
      <tr>
        <th>Runtime</th>
        <td>${submission.runtime}</td>
      </tr>
      % if submission.judgement:
        <tr>
          <th>Grade</th>
          <td>${submission.judgement.grade}</td>
        </tr>
      % endif
    % else:
      <p>Submission is not yet finished.</p>
    % endif
  </table>

  <h3>Source code:</h3>
  % if submission.source:
    <p class="btn-group">
      <a href="${submission.url}/source" class="btn btn-mini"><i class="icon-file"></i> Full page</a>
      <a href="${submission.url}/download" class="btn btn-mini"><i class="icon-download-alt"></i> Download</a>
    </p>

  <div>
    ${c.pygmentize.display(id="source_container", lexer=submission.language.lexer_name, source=submission.source) | n}
  </div>

  % else:
    <p>No source code submitted yet.</p>
  % endif
  
</%def>

<%def name="details_judgement(judgement)">

  % if judgement.annotations:
  <h4>Annotations:</h4>
    <table>
    % for line, ann in sorted(judgement.annotations.iteritems()):
      <tr>
        <th>
          <a href="javascript:highline('source_container', 'line-${line}')">Line ${line}</a>
        </th>
        <td>
          ${ann}
        </td>
      </tr>
    % endfor
    </table>
  % endif

  % if judgement.comment:
    <h4>Comment:</h4>
    <p>${judgement.comment}</p>
  % endif

  % if judgement.corrected_source:
    <h4>Corrected source code:</h4>
    <p>
      <a href="${judgement.submission.url}/source/judgement" class="btn btn-mini">Full page</a>,
      <a href="${judgement.submission.url}/download/judgement" class="btn btn-mini">Download</a>
    </p>
    ${c.pygmentize.display(lexer=judgement.submission.language.lexer_name, source=judgement.corrected_source) | n}

    <h4>Diff</h4>
    ${c.pygmentize.display(lexer='diff', source=judgement.diff) | n}
  % endif

</%def>

<%def name="compilation(compilation)">

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

</%def>