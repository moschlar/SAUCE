<%inherit file="local:templates.master" />

<%def name="title()">
  Similarity ${view}
</%def>

<%def name="submission_details(submission)">
  <dl class="dl-horizontal">
    <dt>Submission:</dt>
    <dd>
      <a href="${submission.url}" style="color: white">
        <span class="badge ${'' if submission.result is None else ('badge-success' if submission.result else 'badge-error')}">
          ${submission.id}
        </span>
      </a>
    </dd>
  </dl>
  <dl class="dl-horizontal">
    <dt>User:</dt>
    <dd>${submission.user.display_name}</dd>
    % if submission.team:
      <dt>Team:</dt>
      <dd>${submission.team}</dd>
    % endif
    <dt>Created:</dt>
    <dd>${submission.created.strftime('%c')}</dd>
    <dt>Last modified:</dt>
    <dd>${submission.modified.strftime('%c')}</dd>
  </dl>
</%def>

<div class="page-header">
  <h1>Similarity ${view}
    % if assignment:
      <small>for Assignment: ${assignment.link}</small>
    % endif
  </h1>
</div>

<div class="row">
  <div class="offset1 span5"><div class="">
    ${submission_details(a)}
  </div></div>
  <div class="span5"><div class="">
    ${submission_details(b)}
  </div></div>
</div>

<div class="row">
  <div class="offset4 span4">
    <div class="" style="text-align: center;">
      <dl class="dl-horizontal">
        <dt>Similarity value:</dt>
        <dd style="color: ${c.rgb(x)}">${'%.2f' % (1 - x)}</dd>
      </dl>
    </div>
  </div>
</div>

<div class="row">
  <div class="span12">
    ${c.pygmentize.display(id="source_container", lexer='diff', source=source) | n}
  </div>
</div>
