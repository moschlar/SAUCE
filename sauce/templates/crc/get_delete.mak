<%inherit file="local:templates.master"/>
<%namespace file="local:templates.crc.menu" import="crud_menu" />

<%def name="title()">
  Delete ${hasattr(c, 'menu_item') and c.menu_item or model}
</%def>

<div id="main_content" class="row">
  ${crud_menu(pk_count)}
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>${self.title()}</h1>
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
