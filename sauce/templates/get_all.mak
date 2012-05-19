<%inherit file="local:templates.master"/>
<%namespace name="menu_items" file="tgext.crud.templates.menu_items"/>

<%def name="title()">
${tmpl_context.title} - ${model} Listing
</%def>
<%def name="header()">
${menu_items.menu_style()}
<script>
    function crud_search_field_changed(select) {
        var selected = '';
        for (var idx=0; idx != select.options.length; ++idx) {
            if (select.options[idx].selected)
                selected = select.options[idx];
        }
        var field = document.getElementById('crud_search_value');
        field.name = selected.value;
    }
</script>
${parent.header()}
</%def>
<%def name="body_class()">tundra</%def>
<div id="main_content">
  ${menu_items.menu_items()}
  <div id="crud_content">
    <h1>${model} Listing</h1>
    <div id="crud_btn_new">
    % if hasattr(tmpl_context, 'btn_new') and not tmpl_context.btn_new:
      &nbsp;
    % else:
      <a href='${tg.url("new", params=tmpl_context.kept_params)}' class="add_link">New ${model}</a>
    % endif
         % if tmpl_context.paginators:
           <span>${tmpl_context.paginators.value_list.pager(link=mount_point+'/')}</span>
         % endif
      <div id="crud_search">
          <form>
              <select id="crud_search_field" onchange="crud_search_field_changed(this);">
                  <option value="${headers[0][0]}" selected="selected">${headers[0][1]}</option>
                  % for field,name in headers[1:]:
                  <option value="${field}">${name}</option>
                  % endfor
              </select>
              <input id="crud_search_value" name="${headers[0][0]}" type="text" placeholder="equals"/>
              <input type="submit" value="Search"/>
          </form>
      </div>
    </div>
    <div class="crud_table">
     ${tmpl_context.widget(value=value_list, action=mount_point+'.json', attrs=dict(style="height:200px; border:solid black 3px;")) |n}
    </div>
  </div>
  <div style="clear:both;"> &nbsp; </div>
</div>
