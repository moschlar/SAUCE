<%inherit file="local:templates.master"/>

<%def name="title()">
  ${event.name} Administration
</%def>

<h2>${event.name} Administration</h2>

<h3>Attention</h3>
<p>Please be careful when filling out forms:<br />
If form validation error occur, you will probably
use the selected values in MultipleSelectFields.</p>

<ul>
% for menu_item in menu_items:
  <li><a href="./admin/${menu_item}s">${menu_item.capitalize()}</a></li>
% endfor
</ul>