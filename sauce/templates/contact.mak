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
  Contact
</%def>

<div class="page-header">
  <h1>SAUCE <small>System for AUtomated Code Evaluation</small></h1>
</div>

<h2>Contact</h2>

<p>There are two different people which you can contact, depending on your
concern at hand:</p>

<div class="row">

<div class="span6">
<h3>Maintainer</h3>
<p>
If you have any questions, problems or issues regarding this specific instance of <strong>SAUCE</strong>,
like the available programming languages or data protection issues,
please contact the maintainer at <a href="mailto:${tg.config.get('email_to')}">${tg.config.get('email_to')}</a>.
</p>
</div>

<div class="span6">
<h3>Developer</h3>
<p>
If you have general questions about <strong>SAUCE</strong> or want to report a bug or an idea
for improvement, you can simply file an <a href="https://github.com/moschlar/SAUCE/issues">issue</a>
in the GitHub issue tracking system or you can contact the
<a href="https://github.com/moschlar">developer</a> directly.
</p>
</div>

</div>
