<%inherit file="local:templates.master"/>
<%namespace file="local:templates.crc.get_all" import="menu_items" />

<%def name="title()">
  Edit ${c.menu_item}
</%def>

<div id="main_content" class="row">
  ${menu_items(pk_count)}
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>Edit ${c.menu_item}</h1>
    </div>
    <div class="crud_edit">
       ${tmpl_context.widget(value=value, action='./') | n}
    </div>
  </div>
</div>
