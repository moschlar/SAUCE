<%!
from sauce.lib.menu import menu_crc
%>

<%def name="crud_menu(pk_count=0)">
  <div id="crud_leftbar" class="span2">
    <div id="menu_items" class="well" style="padding: 9px 0;">
      ${menu_crc(((c.crud_helpers.make_link(url, pk_count), name) for (url, name) in c.menu_items.iteritems()), c.menu_item if hasattr(c, 'menu_item') else model).render(direction='vertical', class_menu='nav nav-list') | n}
    </div>
  </div>
</%def>
