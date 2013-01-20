<%inherit file="local:templates.master"/>
<%namespace file="local:templates.crc.menu" import="crud_menu" />

<%def name="title()">
  New ${getattr(c, 'menu_item', model)}
</%def>

<div id="main_content" class="row">
  ${crud_menu()}
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>${self.title()}</h1>
    </div>
    <div class="crud_add">
       ${tmpl_context.widget(value=value, action='./') | n}
    </div>
  </div>
</div>
