<%inherit file="local:templates.master"/>

<%def name="title()">
  Languages
</%def>

<div class="page-header">
  <h1>Languages</h1>
</div>

% if languages:

  <ul>
  % for l in languages:
    <li><a href="${tg.url('/languages/%d' % l.id)}">${l}</a></li>
  % endfor
  </ul>

% else:
  <p>No languages defined.</p>
% endif
