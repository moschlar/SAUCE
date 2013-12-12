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

<%def name="title()">
  Languages
</%def>

<div class="page-header">
  <h1>Languages</h1>
</div>

% if languages:

<p>These pages allow you to view information about how currently
available programming languages are configured.</p>

  <ul>
  % for l in languages:
    <li><a href="${tg.url('/languages/%d' % l.id)}">${l.name}</a></li>
  % endfor
  </ul>

% else:
  <p>No programming languages defined.</p>
% endif
