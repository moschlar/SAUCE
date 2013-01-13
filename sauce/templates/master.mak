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
  <link rel="icon" href="${tg.url('/favicon.ico')}" type="image/x-icon" />

  <script type="text/javascript" src="${tg.url('/javascript/jquery.js')}"></script>
  <script type="text/javascript" src="${tg.url('/javascript/bootstrap.js')}"></script>
##  <script type="text/javascript" src="${tg.url('/javascript/bootstrap.min.js')}"></script>

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
      <div class="span5">
        <p>&copy; 2012 - ${h.current_year()}
          <a href="mailto:sauce@moritz-schlarb.de">Moritz Schlarb</a>
          - <strong>SAUCE</strong> is <a href="http://www.opensource.org/licenses/BSD-2-Clause">free software</a>
        </p>
        <p>
        <iframe src="${tg.url('/github-buttons/github-btn.html', dict(user='moschlar', repo='SAUCE', type='watch', count='true'))}"
          allowtransparency="true" frameborder="0" scrolling="0" width="110px" height="20px"></iframe>
        <iframe src="${tg.url('/github-buttons/github-btn.html', dict(user='moschlar', repo='SAUCE', type='fork', count='true'))}"
          allowtransparency="true" frameborder="0" scrolling="0" width="110px" height="20px"></iframe>
        </p>
      </div>
      <div class="span1">
        <span class="label" title="Git revision: ${g.revision}">Version: ${g.version}</span>
      </div>
      <div class="offset2 span4">
        <a class="pull-right" href="http://www.turbogears.org/2.2/" title="TurboGears is a open source front-to-back web development framework written in Python. Copyright &copy; 2005-2012">
          <img style="vertical-align:middle;" src="${tg.url('/images/under_the_hood_blue.png')}" alt="TurboGears 2" />
        </a>
      </div>
    </div>
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

            <li class="${('', 'active')[page=='events' or bool(getattr(c, 'event', False))]} dropdown">
              <a class="dropdown-toggle bold" data-toggle="dropdown" data-target="#" href="#">Events <b class="caret"></b></a>
              
              <ul class="dropdown-menu">
                <li><a href="${tg.url('/events')}"><i class=" icon-th-list"></i>&nbsp;Listing</a></li>
                % for heading, l in ((None, c.current_events), ('Future', c.future_events), ('Previous', c.previous_events)):
                  % if l:
                    <li class="divider"></li>
                    % if heading:
                      <li class="nav-header">${heading}</li>
                    % endif
                    % for event in l:
                      <li>
                        <a href="${event.url}">${event.name}
                        % if not event.public:
                          <i class="icon-lock"></i>
                        % endif
                        </a>
                      </li>
                    % endfor
                  % endif
                % endfor
              </ul>
            </li>

            <li class="divider-vertical"></li>

            <li class="${('', 'active')[page=='news']}">
              ${h.link_to('News', tg.url('/news'))}
            </li>

##            <li class="${('', 'active')[page=='about']}">
##              ${h.link_to('About', tg.url('/about'))}
##            </li>

            <li class="${('', 'active')[page in ('docs', 'about')]} dropdown">
              <a class="dropdown-toggle" data-toggle="dropdown" data-target="#" href="#">
                Documentation <b class="caret"></b>
              </a>
              <ul class="dropdown-menu">
##                <li><a href="${tg.url('/docs')}"><i class="icon-th-list"></i>&nbsp;Listing</a></li>
                <li><a href="${tg.url('/about')}"><i class="icon-info-sign"></i>&nbsp;About</a></li>
                <li class="divider"></li>
                % for doc_label, doc_url in g.doc_list:
                  <li>
                    <a href="${doc_url}">${doc_label}</a>
                  </li>
                % endfor
              </ul>
            </li>

            <li class="${('', 'active')[page=='contact']}">
              ${h.link_to('Contact', tg.url('/contact'))}
            </li>


          </ul>
          
          <ul class="nav nav-pills pull-right">
            % if not request.identity:
              <li>
                <a href="${tg.url('/login', dict(came_from=tg.url(request.environ['PATH_INFO'])))}">
                  <i class="icon-off icon-white"></i>&nbsp;Login
                </a>
              </li>
            % else:
              % if 'manage' in request.identity.get('permissions'):
                <li class="${('', 'active')[page=='admin']}">
                  <a href="${tg.url('/admin')}"><i class="icon-cog icon-white"></i>&nbsp;Admin</a>
                </li>
              % endif
              <li class="${('', 'active')[page=='user']}">
                <a href="${tg.url('/user')}"><i class="icon-user icon-white"></i>&nbsp;${request.identity.get('user')}</a>
              </li>
              <li><a href="${tg.url('/logout_handler')}"><i class="icon-off icon-white"></i>&nbsp;Logout</a></li>
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
