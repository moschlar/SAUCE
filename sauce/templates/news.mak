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

<%inherit file="local:templates.master" />

<%def name="title()">
  News
</%def>

<div class="page-header">
  <h1>News</h1>
</div>

% if news:
  ${news_list(news)}
  <p>${c.paginators.news.pager('Pages: $link_previous ~2~ $link_next')}</p>
% endif

<%def name="news_list(news)">
  <dl>
  % for newsitem in news:
    <dt>${newsitem.subject}
      % if not newsitem.public:
        <i class="icon-lock"></i>
      % endif
    </dt>
    <dd>
      <em>Posted by ${newsitem.user.link} - <span title="${h.strftime(newsitem.date, human=False)}">${h.strftime(newsitem.date, human=True)}</span></em>
      <p>${newsitem.message | n}</p>
    </dd>
  % endfor
  </dl>
</%def>
