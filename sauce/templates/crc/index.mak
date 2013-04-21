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
