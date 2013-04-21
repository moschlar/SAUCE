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

<%!
from sauce.lib.menu import menu_crc
%>

<%def name="crud_menu(pk_count=0)">
  <div id="crud_leftbar" class="span2">
    <div id="menu_items" class="well" style="padding: 9px 0;">
      ${menu_crc(((c.crud_helpers.make_link(url, pk_count), name) for (url, name) in c.menu_items.iteritems()), getattr(c, 'menu_item', model)).render(direction='vertical', class_menu='nav nav-list') | n}
    </div>
  </div>
</%def>
