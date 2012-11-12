<%inherit file="local:templates.master"/>
<%namespace file="local:templates.crc.get_all" import="menu_items" />

<%def name="title()">
  ${event.name} - Administration
</%def>

<div class="row">
  <div class="span2">
    <div class="well" style="padding: 9px 0">
        <ul class="nav nav-list">
          <li class="nav-header">Menu</li>
           % for lower, item in sorted(tmpl_context.menu_items.iteritems()):
            <li>
                <a href="${event.url}/admin/${tmpl_context.crud_helpers.make_link(lower, -1)}">${item}</a>
            </li>
           % endfor
        </ul>
    </div>  </div>
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
