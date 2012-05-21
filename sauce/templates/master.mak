<%
  flash = tg.flash_obj.render('flash', use_js=False)
%>

<!DOCTYPE html>
<html>

<%def name="meta()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</%def>

<%def name="headers()"></%def>
<%def name="title()"></%def>

<head>
  ${self.meta()}
  ${self.headers()}
  <title>${self.title()} - ${g.title}</title>
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap.min.css')}" />
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap-responsive.min.css')}" />
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />

<style type="text/css">
  ${getattr(c, 'style', '')}
  ${h.style}
</style>

</head>

<%def name="body_class()"><% if c.breadcrumbs or c.navigation: return "navbar_left" %></%def>

<body class="${self.body_class()} ${next.body_class()}">
<a href="http://github.com/moschlar/SAUCE"><img style="position: absolute; top: 0; right: 0; border: 0; z-index: 16;" src="https://a248.e.akamai.net/assets.github.com/img/4c7dc970b89fd04b81c8e221ba88ff99a06c6b61/687474703a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f77686974655f6666666666662e706e67" alt="Fork me on GitHub"></a>
  <div class="container">
    ${self.main_menu()}
    % if flash:
      <div class="row"><div class="span8 offset2">
        ${flash | n}
      </div></div>
    % endif
    ${self.body()}

${self.navbar_left()}

    ${self.footer()}
  </div>
</body>

<%def name="footer()">
  <footer class="footer hidden-tablet hidden-phone">
    <a class="pull-right" href="http://www.turbogears.org/2.2/" title="TurboGears is a open source front-to-back web development framework written in Python. Copyright &copy; 2005-2012">
      <img style="vertical-align:middle;" src="${tg.url('/images/under_the_hood_blue.png')}" alt="TurboGears 2" />
    </a>
    <p>&copy; ${h.current_year()}
      <a href="mailto:moschlar@students.uni-mainz.de">Moritz Schlarb</a>
      - ${g.title} is <a href="http://www.opensource.org/licenses/BSD-2-Clause">free software</a>
    </p>
  </footer>
</%def>

<%def name="main_menu()">
  <div class="navbar">
    <div class="navbar-inner">
      <div class="container">
        <a class="brand" href="#">
          <img src="${tg.url('/images/turbogears_logo.png')}" alt="TurboGears 2"/>
          ${g.title}
        </a>
        <ul class="nav">
          <li class="${('', 'active')[page=='index']}">
            <a href="${tg.url('/')}" class="${('', 'active')[page=='index']}">Home</a></li>
          <li class="${('', 'active')[page=='news']}">
            ${h.link_to('News', tg.url('/news'))}</li>
          <li class="${('', 'active')[page=='about']}">
            ${h.link_to('About', tg.url('/about'))}</li>
          <li class="${('', 'active')[page=='docs']}">
            ${h.link_to('Documentation', tg.url('/docs'))}</li>
          <li class="${('', 'active')[page=='events']}">
            ${h.link_to('Contact', tg.url('/contact'))}</li>
          <li class="bold ${('', 'active')[page=='events' or bool(getattr(c, 'event', False))]}">
            ${h.link_to('Events', tg.url('/events'))}</li>
        </ul>
        <ul class="nav pull-right">
          % if not request.identity:
            <li>
              <a href="${tg.url('/login', dict(came_from=tg.url(request.environ['PATH_INFO'])))}">Login</a>
            </li>
          % else:
            % if 'manage' in request.identity.get('permissions'):
              <li><a href="${tg.url('/admin')}">Admin</a></li>
            % endif
            <li class="${('', 'active')[page=='user']}">
              <a href="${tg.url('/admin')}">${request.identity.get('user')}</a>
            </li>
            <li><a href="${tg.url('/logout_handler')}">Logout</a></li>
          % endif
        </ul>
      </div>
    </div>
  </div>
</%def>

<%def name="navbar_left()">
% if c.breadcrumbs or c.navigation:
  <div id="navbar_left">
    <h2>Menu</h2>
    % if c.breadcrumbs:
    <h3>Breadcrumbs</h3>
      <ul class="links">
        % for breadcrumb in c.breadcrumbs:
          <li>${breadcrumb | n}</li>
        % endfor
      </ul>
    % endif

    % if c.navigation:
    <h3>Navigation</h3>
      <ul class="links">
        % for link in c.navigation:
          % if isinstance(link, list):
            <li>${link[0] | n}</li>
            <ul class="links">
              % for l in link[1:]:
                <li>${l | n}</li>
              % endfor
            </ul>
          % else:
            <li>${link | n}</li>
          % endif
        % endfor
      </ul>
    % endif
    </div>
% endif
</%def>

</html>
