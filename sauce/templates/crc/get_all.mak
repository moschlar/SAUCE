## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

<%inherit file="local:templates.master"/>
<%namespace file="local:templates.crc.menu" import="crud_menu" />

<%def name="title()">
  ${getattr(c, 'menu_item', model)} Listing
</%def>

<%def name="header()">
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

<div id="main_content" class="row">
  ${crud_menu()}
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>${self.title()}</h1>
    </div>
    <div class="row">
    <div id="crud_btn_new" class="span2">
    % if getattr(tmpl_context, 'allow_new', True):
      <a href='${tg.url("new", params=tmpl_context.kept_params)}' class="btn"><i class="icon-plus-sign"></i>&nbsp;New ${model}</a>
    % else:
      &nbsp;
    % endif
    </div>
    <div class="span2" style="padding: 4px 0;">
      <span class="badge">${len(value_list)}</span>
    </div>
    <div class="span2">
         % if tmpl_context.paginators:
           <span>${tmpl_context.paginators.value_list.pager(link=mount_point+'/')}</span>
         % else:
           &nbsp;
         % endif
    </div>
    <div class="span4">
      <div id="crud_search" class="pull-right">
        <form class="form-search">
            <select id="crud_search_field" onchange="crud_search_field_changed(this);" class="input-small">
                <option value="${headers[0][0]}" selected="selected">${headers[0][1]}</option>
                % for field,name in headers[1:]:
                <option value="${field}">${name}</option>
                % endfor
            </select>
            <input id="crud_search_value" name="${headers[0][0]}" type="text" placeholder="equals" class="search-query input-small" />
            <button type="submit" class="btn"><i class="icon-search"></i>&nbsp;Search</button>
        </form>
      </div>
    </div>
    </div>
    <div class="crud_table">
     ${tmpl_context.widget(value=value_list, action=mount_point+'.json') |n}
    </div>
  </div>
  <div style="clear:both;"> &nbsp; </div>
</div>
