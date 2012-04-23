<%
  flash = tg.flash_obj.render('flash', use_js=False)
%>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>

<%def name="meta()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="headers()"></%def>
<%def name="title()"></%def>

<head>
  ${self.meta()}
  <title>${self.title()} - ${g.title}</title>
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/admin.css')}" />
  ${self.headers()}

% if hasattr(c, 'style'):
  <style type="text/css">
    ${c.style}
  </style>
% endif

</head>

<%def name="body_class()"></%def>

<body ${self.body_class()}>
  ${self.header()}
  ${self.main_menu()}
  <div id="wrapper">
    ${self.navbar_left()}
    <div id="content">
% if flash:
      ${flash | n}
% endif
      ${self.body()}
    </div>
    ${self.footer()}
  </div>
</body>

<%def name="header()">
<a href="http://github.com/moschlar/SAUCE"><img style="position: absolute; top: 0; right: 0; border: 0; z-index: 16;" src="https://a248.e.akamai.net/assets.github.com/img/4c7dc970b89fd04b81c8e221ba88ff99a06c6b61/687474703a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f77686974655f6666666666662e706e67" alt="Fork me on GitHub"></a>
  <div id="header">
    <h1><a href="${tg.url('/')}">${g.title}</a><br />
        <span class="subtitle">${g.subtitle}</span>
    </h1>
% if hasattr(g, 'version'):
    <h3>Version ${g.version}</h3>
% endif
  </div>
</%def>

<%def name="footer()">
  <div class="clearingdiv"></div>
  <hr style="margin-top:50px" />
  <div class="fcenter">
    <p>&copy; 2012 <a href="mailto:moschlar@students.uni-mainz.de">Moritz Schlarb</a> - ${g.title} is <a href="http://www.opensource.org/licenses/BSD-2-Clause">free software</a></p>
    <p><a href="http://www.turbogears.org/" title="TurboGears is a open source front-to-back web development framework written in Python. Copyright &copy; 2005-2012">
      <img src="${tg.url('/images/under_the_hood_blue.png')}" alt="TurboGears 2" /><br />
      Powered by TurboGears 2
    </a></p>
  </div>
  <div class="clearingdiv"></div>
</%def>

<%def name="main_menu()">
  <ul id="mainmenu">
    <li class="first"><a href="${tg.url('/')}" class="${('', 'active')[page=='index']}">Home</a></li>
    <li>${h.link_to('News', tg.url('/news'), class_=('', 'active')[page=='news'])}</li>
    <li>${h.link_to('About', tg.url('/about'), class_=('', 'active')[page=='about'])}</li>
    <li>${h.link_to('Contact', tg.url('/contact'), class_=('', 'active')[page=='contact'])}</li>
    <li class="bold">${h.link_to('Events', tg.url('/events'), class_=('', 'active')[page=='events'])}</li>
% if tg.auth_stack_enabled:
    <span>
      % if not request.identity:
        <li id="login" class="loginlogout">
          <a href="${tg.url('/login', dict(came_from=tg.url(request.environ['PATH_INFO'])))}">Login</a>
        </li>
      % else:
        <li id="login" class="loginlogout"><a href="${tg.url('/logout_handler')}">Logout</a></li>
        <li id="identity" class="loginlogout ${('', 'active')[page=='user']}"><a href="/user">${request.identity.get('user')}</a></li>
        % if 'manage' in request.identity.get('permissions'):
          <li id="admin" class="loginlogout"><a href="${tg.url('/admin')}">Admin</a></li>
        % endif
      % endif
    </span>
% endif
  </ul>
</%def>

<%def name="navbar_left()">
% if navigation or bread:
  <div id="navbar_left">
    <h2>Menu</h2>
    % if bread:
    <h3>Breadcrumbs</h3>
      <ul class="links">
        % for breadcrumb in bread.breadcrumbs:
          <li>${breadcrumb | n}</li>
        % endfor
      </ul>
    % endif
    % if navigation:
    <h3>Navigation</h3>
      <ul class="links">
        % for link in navigation:
          <li>${link | n}</li>
        % endfor
      </ul>
    % endif
    </div>
% endif
</%def>

</html>
