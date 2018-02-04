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

<!DOCTYPE html>
<html>

<%def name="meta()">
  <meta content="text/html; charset=${response.charset}" http-equiv="content-type" />
  <meta charset="${response.charset}" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</%def>

<%def name="headers()"></%def>
<%def name="title()"></%def>

<head>
  <title>${self.title()} - ${g.title}</title>

  ${self.meta()}

  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap.min.css')}" />
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
##  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap-responsive.min.css')}" />
  <link rel="icon" href="${tg.url('/favicon.ico')}" type="image/x-icon" />

  <script type="text/javascript" src="${tg.url('/javascript/jquery.js')}"></script>
  <script type="text/javascript" src="${tg.url('/javascript/bootstrap.js')}"></script>
##  <script type="text/javascript" src="${tg.url('/javascript/bootstrap.min.js')}"></script>

  ${self.headers()}

</head>

<%def name="body_class()"></%def>

<body class="${self.body_class()} ${next.body_class()}">
  <div class="container">
    ${self.main_menu()}
    ${self.sub_menu()}
    ${self.flash()}

    <div class="row">
      % if c.side_menu:
        <div class="span3">
          ${self.side_menu()}
        </div>

        <div class="span9">
      % else:
        <div class="span12">
      % endif
      ${next.body()}
      </div>
    </div>

    ${self.footer()}
  </div>

<%include file="local:templates.foot" />

</body>

<%def name="footer()">
  <footer class="footer hidden-tablet hidden-phone">
    <div class="row">
      <div class="span3">
        <p>&copy; 2012 - ${h.current_year()}
          <a href="https://github.com/moschlar">Moritz Schlarb</a>
          <br />
          <strong>SAUCE</strong> is <a href="http://opensource.org/licenses/AGPL-3.0">free software</a>
        </p>
      </div>
      <div class="span1" style="text-align: left; vertical-align: middle;">
<a href="http://opensource.org/licenses/AGPL-3.0" title="AGPL-3.0">\
<img style="vertical-align: middle;" src="${tg.url('/images/agplv3-88x31.png')}" alt="AGPL-3.0" />\
</a>
      </div>
      <div class="offset1 span2" style="text-align: center; vertical-align: middle;">
        <p style="vertical-align: middle;"><span class="label" title="Git revision: ${g.revision}">Version: ${g.version}</span></p>
      </div>
      <div class="offset1 span2" style="text-align: right; vertical-align: middle; ">
<a href="http://www.python.org/" title="Python">\
<img style="vertical-align: middle;" src="${tg.url('/images/python-logo.gif')}" alt="Python" />\
</a>
        <br />
<a href="http://www.sqlalchemy.org/" title="SQLAlchemy">\
<img style="vertical-align: middle; padding-right: 8px;" src="${tg.url('/images/sqla-logo6.gif')}" width="88" alt="SQLAlchemy" />\
</a>
      </div>
      <div class="span2" style="text-align: right;vertical-align: middle; ">
<a href="http://www.turbogears.org/" title="TurboGears is a open source front-to-back web development framework written in Python. Copyright &copy; 2005-2012">\
<img style="vertical-align: middle;" src="${tg.url('/images/under_the_hood_blue.png')}" alt="TurboGears 2" />\
</a>
      </div>
    </div>
    <div class="row">
      <div class="span2">
        <p>
          <iframe src="https://ghbtns.com/github-btn.html?user=moschlar&repo=SAUCE&type=star&count=true" frameborder="0" scrolling="0" width="140px" height="20px"></iframe>
        </p>
      </div>
      <div class="span2">
        <p>
          <iframe src="https://ghbtns.com/github-btn.html?user=moschlar&repo=SAUCE&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="140px" height="20px"></iframe>
        </p>
      </div>
      <div class="span2">
        <p>
          <iframe src="https://ghbtns.com/github-btn.html?user=moschlar&repo=SAUCE&type=fork&count=true" frameborder="0" scrolling="0" width="140px" height="20px"></iframe>
        </p>
      </div>
    </div>
  </footer>
</%def>

<%def name="flash()">
  <%
    flash = tg.flash_obj.render('flash', use_js=False)
  %>
  % if flash:
    <div class="row"><div class="span8 offset2">
      ${flash | n}
    </div></div>
  % endif
</%def>

<%def name="main_menu()">
  <div class="navbar navbar-fixed-top">
    <div class="navbar-inner">
      <div class="container">
        <!-- .btn-navbar is used as the toggle for collapsed navbar content -->
        <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </a>

        <a class="brand" href="${tg.url('/')}" title="${g.subtitle}">
          <img src="${tg.url('/images/sauce_logo.png')}" alt="SAUCE"/>
          SAUCE
        </a>

        <!-- Everything you want hidden at 940px or less, place within here -->
        <div class="nav-collapse">
          <ul class="nav nav-pills">
            <li class="${('', 'active')[page=='index']}">
              <a href="${tg.url('/')}">Home</a>
            </li>

            <li class="divider-vertical"></li>

            ${c.event_menu.render(direction="dropdown", class_dropdown='dropdown bold' + ('', ' active')[page=='events' or bool(getattr(c, 'event', False))]) | n}

            <li class="divider-vertical"></li>

            <li class="${('', 'active')[page=='news']}">
              ${h.link_to('News', tg.url('/news'))}
            </li>

            ${c.doc_menu.render(direction="dropdown", class_dropdown='dropdown' + ('', ' active')[page in ('docs', 'about', 'language')]) | n}

            <li class="${('', 'active')[page=='contact']}">
              ${h.link_to('Contact', tg.url('/contact'))}
            </li>

          </ul>

          <ul class="nav nav-pills pull-right">
            % if not request.identity:
              <li>
                <a href="${h.make_login_url()}">
                  <i class="icon-off icon-white"></i>&nbsp;Login
                </a>
              </li>
			% if h.show_registration():
			  <li>
				<a href="${tg.url('/registration')}">
				  <i class="icon-asterisk icon-white"></i>&nbsp;Register
				</a>
			  </li>
              % endif
            % else:
              % if 'manage' in request.identity.get('permissions'):
                <li class="${('', 'active')[page=='admin']}">
                  <a href="${tg.url('/admin')}"><i class="icon-cog icon-white"></i>&nbsp;Admin</a>
                </li>
              % endif
              <li class="${('', 'active')[page=='user']}">
                <a href="${tg.url('/user')}"><i class="icon-user icon-white"></i>&nbsp;${request.identity.get('user')}</a>
              </li>
              <li>
                <a href="${h.make_logout_url()}">
                  <i class="icon-off icon-white"></i>&nbsp;Logout
                </a>
              </li>
            % endif
          </ul>
        </div>
      </div>
    </div>
  </div>
</%def>

<%def name="sub_menu()">
% if c.sub_menu:
  <div class="navbar">
    <div class="navbar-inner">
      <div class="container">
        ${c.sub_menu.render(direction='horizontal') | n}
      </div>
    </div>
  </div>
% endif
</%def>

<%def name="side_menu()">
  <div class="well" style="padding: 9px 0">
    % if c.side_menu:
      ${c.side_menu.render(class_menu='nav-list') | n}
    % endif
  </div>
</%def>

</html>
