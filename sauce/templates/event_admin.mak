<%inherit file="local:templates.master"/>

<%def name="title()">
  ${event.name} Administration
</%def>

<div style="height:0px;"> &nbsp; </div>
    <h2>${event.name} Admin</h2>

<ul>
% for menu_item in menu_items:
  <li><a href="./admin/${menu_item}s">${menu_item.capitalize()}</a></li>
% endfor
</ul>