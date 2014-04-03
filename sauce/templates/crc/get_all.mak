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

<%def name="headers()">
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
<script type="text/javascript">
function show_processing_modal(text) {
    var modaldiv = $('<div class="modal hide" id="pleaseWaitDialog" data-backdrop="static" data-keyboard="false"><div class="modal-header"><h1>Processing...</h1></div><div class="modal-body"><p>' + (text || '') + '</p><div class="progress progress-striped active"><div class="bar" style="width: 100%;"></div></div></div></div>');
    modaldiv.modal();
}
</script>
${parent.headers()}
</%def>

<div id="main_content" class="row">
  ${crud_menu()}
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>${self.title()}</h1>
    </div>
    <div class="row">
    <div id="crud_btn_new" class="span4">
      ${c.bulk_actions | n}
    </div>
    <div class="span1" style="padding: 4px 0;">
      <span class="badge">${len(value_list)}</span>
    </div>
    <div class="span5">
      % if search_fields:
        <div id="crud_search" class="pull-right">
          <form class="form-search">
              <select id="crud_search_field" class="input-small" onchange="crud_search_field_changed(this);">
                  % for field, name, selected in search_fields:
                    % if selected is not False:
                      <option value="${field}" selected="selected">${name}</option>
                    % else:
                      <option value="${field}">${name}</option>
                    % endif
                  % endfor
              </select>
              <input id="crud_search_value" class="search-query input-small" name="${current_search[0]}" type="text" placeholder="equals / contains" value="${current_search[1]}" />
              <button type="submit" class="btn"><i class="icon-search"></i>&nbsp;Search</button>
          </form>
        </div>
      % endif
    </div>
    </div>
    <div class="crud_table">
     ${tmpl_context.widget(value=value_list, action=mount_point+'.json') |n}
    </div>
    <div class="row">
      <div class="offset2 span3">
         % if tmpl_context.paginators:
           <span>${tmpl_context.paginators.value_list.pager(link=mount_point+'/')}</span>
         % else:
           &nbsp;
         % endif
      </div>
    </div>
  </div>
  <div style="clear:both;"> &nbsp; </div>
</div>
