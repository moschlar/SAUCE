<%inherit file="/base.mako" />

<h1>System for AUtomated Code Evaluation</h1>
<h2>${c.site}</h2>

<h3>Assignments:</h3>
% for assignment in c.assignments:
  <h4><a href="${url(controller='assignment', action='show', id=assignment.id)}">${assignment.title}</a></h4>
  <p>${assignment.description}</p>
% endfor
${c.assignments.pager('$link_previous ~2~ $link_next')}