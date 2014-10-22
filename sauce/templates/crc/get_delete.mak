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
  Delete ${getattr(c, 'menu_item', model)}
</%def>

<div id="main_content" class="row">
  % if getattr(c, 'show_menu', True):
    ${crud_menu(pk_count)}
  % endif
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>${self.title()}</h1>
    </div>
    <div class="crud_delete">
       <p>
         You are about to delete ${unicode(obj)} persistently from the database!<br />
       </p>
       % if deps != u'<dl></dl>':
         <p>
           This will also delete:<br />
           ${deps | n}
         </p>
       % endif
       <p>
         Are you totally sure to delete this entry?
       </p>
           <form method="POST" action="../${pklist}">
             <a href=".." class="btn">Cancel</a>
             <input type="hidden" name="_method" value="DELETE" />
             <button type="submit" class="btn btn-danger">
               <i class="icon-remove icon-white"></i>&nbsp;Delete&nbsp;${unicode(obj)}
             </button>
           </form>
    </div>
  </div>
</div>
