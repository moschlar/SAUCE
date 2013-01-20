<%inherit file="local:templates.master"/>
<%namespace file="local:templates.crc.menu" import="crud_menu" />

<%def name="title()">
  ${c.title} - Administration
</%def>

<div id="main_content" class="row">
  ${crud_menu(-1)}
  <div id="crud_content" class="span10">
    <div class="page-header">
      <h1>${self.title()}</h1>
    </div>
  </div>
  <div style="clear:both;"> &nbsp; </div>
</div>
