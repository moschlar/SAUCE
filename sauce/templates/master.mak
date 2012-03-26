<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    ${self.meta()}
    <title>${self.title()} - ${g.title}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/admin.css')}" />
    ${self.headers()}
</head>
<body class="${self.body_class()}">
  ${self.header()}
  ${self.main_menu()}
  ${self.content_wrapper()}
  ${self.footer()}
</body>

<%def name="content_wrapper()">
<div id="wrapper">
  ${self.navbar_left()}
 <div id="content">
<%
  flash=tg.flash_obj.render('flash', use_js=False)
%>
% if flash:
  ${flash | n}
% endif
  ${self.body()}
</div>
</%def>

<%def name="body_class()"> </%def>

<%def name="meta()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>
<%def name="headers()">
</%def>
<%def name="title()"> </%def>

<%def name="header()">
<a href="http://github.com/moschlar/SAUCE"><img style="position: absolute; top: 0; right: 0; border: 0; z-index: 16;" src="https://a248.e.akamai.net/assets.github.com/img/4c7dc970b89fd04b81c8e221ba88ff99a06c6b61/687474703a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f77686974655f6666666666662e706e67" alt="Fork me on GitHub"></a>
  <div id="header">
    <h1>${g.title}<br />
        <span class="subtitle">${g.subtitle}</span>
    </h1>
    <h3>${g.version}</h3>
  </div>
</%def>

<%def name="footer()">
  <div class="clearingdiv"></div>
  <hr style="margin-top:50px" />
  <div class="fcenter">
##    <p>&copy; 2012 <a href="http://www.moritz-schlarb.de">Moritz Schlarb</a> - ${g.title} is <a href="http://www.opensource.org/licenses/bsd-license.php">free software</a></p>
    <p>&copy; 2012 <a href="mailto:moschlar@students.uni-mainz.de">Moritz Schlarb</a> - ${g.title} is <a href="http://www.opensource.org/licenses/bsd-license.php">free software</a></p>
    <p><a href="http://www.turbogears.org/" title="TurboGears is a open source front-to-back web development framework written in Python. Copyright &copy; 2005-2012">
      <img src="${tg.url('/images/under_the_hood_blue.png')}" alt="TurboGears 2" /><br />
      Powered by TurboGears 2
    </a></p>
  </div>
  <div class="clearingdiv"></div>
</div>
</%def>

<%def name="main_menu()">
  <ul id="mainmenu">
    <li class="first"><a href="${tg.url('/')}" class="${('', 'active')[page=='index']}">Home</a></li>
##        <li><a href="${tg.url('/environ')}" class="${('', 'active')[page=='environ']}">WSGI Environment</a></li>
        <li>${h.html.tags.link_to('News', tg.url('/news'), class_=('', 'active')[page=='news'])}</li>
        <li>${h.html.tags.link_to('Events', tg.url('/events'), class_=('', 'active')[page=='events'])}</li>
    % if tg.auth_stack_enabled:
      <span>
          % if not request.identity:
            <li id="login" class="loginlogout"><a href="${tg.url('/login')}">Login</a></li>
          % else:
            <li id="login" class="loginlogout"><a href="${tg.url('/logout_handler')}">Logout</a></li>
            <li id="identity" class="loginlogout"><a href="#">${request.identity.get('user')}</a></li>
            % if 'manage' in request.identity.get('permissions'):
              <li id="admin" class="loginlogout"><a href="${tg.url('/admin')}">Admin</a></li>
            % endif
          % endif
      </span>
    % endif
  </ul>
</%def>

<%def name="navbar_left()">
% if event:
  <div id="navbar_left">
      <h2>${event.name}</h2>
      <ul class="links">
        <li>${h.link('Event', tg.url('/events/%d' % (event.id)), class_=('', 'bold')[page=='events'])}</li>
        <li>${h.link('Assignments', tg.url('/events/%d/assignments' % (event.id)), class_=('', 'bold')[page=='assignments'])}</li>
    % if request.student:
        <li>${h.link('Submissions', tg.url('/events/%d/submissions' % (event.id)), class_=('', 'bold')[page=='submissions'])}</li>
    % endif
        <li>${h.link('Scores', tg.url('/events/%d/scores' % (event.id)), class_=('', 'bold')[page=='scores'])}</li>
      </ul>
  </div>
% endif
</%def>

</html>
