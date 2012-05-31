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
  ${self.meta()}
  ${self.headers()}
  <title>${self.title()} - ${g.title}</title>
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap.min.css')}" />
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
  <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/bootstrap-responsive.min.css')}" />

  <script src="${tg.url('/javascript/jquery.js')}"></script>
  <script src="${tg.url('/javascript/bootstrap.js')}"></script>
##  <script src="${tg.url('/javascript/bootstrap.min.js')}"></script>

##<style type="text/css">
##  ${getattr(c, 'style', '')}
##  ${h.style}
##</style>

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
</body>

<%def name="footer()">
  <footer class="footer hidden-tablet hidden-phone">
    <a class="pull-right" href="http://www.turbogears.org/2.2/" title="TurboGears is a open source front-to-back web development framework written in Python. Copyright &copy; 2005-2012">
      <img style="vertical-align:middle;" src="${tg.url('/images/under_the_hood_blue.png')}" alt="TurboGears 2" />
    </a>
    <p>&copy; ${h.current_year()}
      <a href="mailto:moschlar@students.uni-mainz.de">Moritz Schlarb</a>
      - <strong>SAUCE</strong> is <a href="http://www.opensource.org/licenses/BSD-2-Clause">free software</a>
    </p>
    <p>
    <iframe src="http://markdotto.github.com/github-buttons/github-btn.html?user=moschlar&repo=SAUCE&type=watch&count=true"
      allowtransparency="true" frameborder="0" scrolling="0" width="110px" height="20px"></iframe>
    <iframe src="http://markdotto.github.com/github-buttons/github-btn.html?user=moschlar&repo=SAUCE&type=fork&count=true"
      allowtransparency="true" frameborder="0" scrolling="0" width="110px" height="20px"></iframe>
    </p>
  </footer>
</%def>

<%def name="flash()">
  <%
    flash = tg.flash_obj.render('flash', use_js=False)
  %>
  % if flash:
  ##TODO: row-fluid does not respect offset, which makes the flash message look displaced in fluid layout
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
        
        <a class="brand" href="${tg.url('/')}">
          <img src="${tg.url('/images/sauce_logo.png')}" alt="SAUCE"/>
          SAUCE
        </a>
        
        <!-- Everything you want hidden at 940px or less, place within here -->
        <div class="nav-collapse">
          <ul class="nav nav-pills">
            <li class="${('', 'active')[page=='index']}">
              <a href="${tg.url('/')}">Home</a>
            </li>
            <li class="${('', 'active')[page=='news']}">
              ${h.link_to('News', tg.url('/news'))}
            </li>
            <li class="${('', 'active')[page=='about']}">
              ${h.link_to('About', tg.url('/about'))}
            </li>
            <li class="${('', 'active')[page=='docs']}">
              ${h.link_to('Documentation', tg.url('/docs'))}
            </li>
            <li class="${('', 'active')[page=='contact']}">
              ${h.link_to('Contact', tg.url('/contact'))}
            </li>
            <li class="${('', 'active')[page=='events' or bool(getattr(c, 'event', False))]} dropdown">
              <a class="dropdown-toggle" data-toggle="dropdown" data-target="#" href="#">Events <b class="caret"></b></a>
              
              <ul class="dropdown-menu">
                <li><a href="${tg.url('/events')}">Listing</a></li>
                <li class="divider"></li>
                % for event in c.events:
                  <li>
                    <a href="${event.url}">${event.name}
                    % if not event.public:
                      <i class="icon-lock"></i>
                    % endif
                    </a>
                  </li>
                % endfor
              </ul>
            </li>
          </ul>
          
          <ul class="nav nav-pills pull-right">
            % if not request.identity:
              <li>
                <a href="${tg.url('/login', dict(came_from=tg.url(request.environ['PATH_INFO'])))}">Login</a>
              </li>
            % else:
              % if 'manage' in request.identity.get('permissions'):
                <li class="${('', 'active')[page=='admin']}">
                  <a href="${tg.url('/admin')}">Admin</a>
                </li>
              % endif
              <li class="${('', 'active')[page=='user']}">
                <a href="${tg.url('/user')}"><i class="icon-user icon-white"></i> ${request.identity.get('user')}</a>
              </li>
              <li><a href="${tg.url('/logout_handler')}">Logout</a></li>
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
