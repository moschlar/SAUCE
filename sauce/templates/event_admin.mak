<%inherit file="local:templates.master"/>
<%namespace file="local:templates.crc.get_all" import="menu_items" />

<%def name="title()">
  ${event.name} - Administration
</%def>

<div class="row">
  ${menu_items(-1, event.url + "/admin/")}
  <div class="span10">
    <div class="page-header">
      <h1>${event.name} <small>Administration</small></h1>
    </div>
    
<h2>Attention</h2>
<p><strong>Please be careful when filling out forms:</strong><br />
If form validation error occur, you will probably
lose the selected values in MultipleSelectFields.</p>

  </div>
</div>
