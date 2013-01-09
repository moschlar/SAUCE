<%inherit file="local:templates.master"/>
<%namespace file="local:templates.crc.get_all" import="menu_items" />

<%def name="title()">
  Delete ${c.menu_item}
</%def>

<div id="main_content" class="row">
  ${menu_items(pk_count)}
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>Delete ${c.menu_item}</h1>
    </div>
    <div class="crud_delete">
       <p>
         You are about to delete ${unicode(obj)} persistently from the database!<br />
       </p>
       <p>
         This will also delete:<br />
         ${deps | n}
       </p>
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
