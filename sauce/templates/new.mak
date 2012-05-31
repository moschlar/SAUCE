<%inherit file="local:templates.master"/>

<%def name="menu_items(pk_count=0)">
  <div id="crud_leftbar" class="span2">
    <div id="menu_items" class="well" style="padding: 9px 0;">
        <ul class="nav nav-list">
          <li class="nav-header">Menu</li>
        % if hasattr(tmpl_context, 'menu_items'):
           % for lower, item in sorted(tmpl_context.menu_items.iteritems()):
            <li class="${('', 'active')[model==item]}">
                <a href="${tmpl_context.crud_helpers.make_link(lower, pk_count)}">${item}</a>
            </li>
           % endfor
        % endif
        </ul>
    </div>
  </div>
</%def>

<%def name="title()">
  New ${model}
</%def>
<%def name="header()">
  ${parent.header()}
</%def>

<div id="main_content" class="row">
  ${menu_items.menu_items()}
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>New ${model}</h1>
    </div>
    <div class="crud_add">
       ${tmpl_context.widget(value=value, action='./') | n}
    </div>
  </div>
</div>
