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

<%def name="times_dl(obj)">

<dl>
% if hasattr(obj, 'start_time'):
  <dt>Start time:</dt>
  <dd title="${h.strftime(obj.start_time, human=False)}">${h.strftime(obj.start_time, human=True)}</dd>
% endif
% if hasattr(obj, 'end_time'):
  <dt>End time:</dt>
  <dd title="${h.strftime(obj.end_time, human=False)}">${h.strftime(obj.end_time, human=True)}</dd>
% endif
% if hasattr(obj, 'is_active'):
  % if obj.is_active:
    <dt>Remaining time:</dt>
    <dd>${h.strftimedelta(obj.remaining_time).decode('utf8')}</dd>
  %endif
% endif
</dl>

</%def>
