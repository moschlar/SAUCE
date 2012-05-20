<%inherit file="local:templates.master"/>

<%def name="title()">
  ${event.name} - Administration
</%def>

<h2>${event.name} - Administration</h2>

<h3>Attention</h3>
<p><strong>Please be careful when filling out forms:</strong><br />
If form validation error occur, you will probably
lose the selected values in MultipleSelectFields.</p>

<h4>Navigation:</h4>
<ul style="list-style-type: None">
% for menu_item in menu_items:
  <li><a href="./admin/${menu_item}s" class="edit_link">${menu_item.capitalize()}</a></li>
% endfor
</ul>