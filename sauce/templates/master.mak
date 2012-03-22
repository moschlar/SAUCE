<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    ${self.meta()}
    <title>${self.title()} - ${g.title}</title>
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/style.css')}" />
    <link rel="stylesheet" type="text/css" media="screen" href="${tg.url('/css/admin.css')}" />
</head>
<body class="${self.body_class()}">
  ${self.header()}
  ${self.main_menu()}
  ${self.content_wrapper()}
  ${self.footer()}
</body>

<%def name="content_wrapper()">
    <div id="content">
    <div>
##    % if page:
##      <div class="currentpage">
##       Now Viewing: <span>${page}</page>
##      </div>
##    % endif
      <%
      flash=tg.flash_obj.render('flash', use_js=False)
      %>
      % if flash:
        ${flash | n}
      % endif
 ${self.sidebar_left()}
      ${self.body()}
    </div>
</%def>

<%def name="body_class()"> </%def>

<%def name="meta()">
  <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>
</%def>

<%def name="title()"> </%def>

<%def name="sidebar_top()">
##  <div id="sb_top" class="sidebar">
##      <h2>Get Started with TG2</h2>
##      <ul class="links">
##        <li>
##          % if page == 'index':
##              <span><a href="${tg.url('/about')}">About this page</a> A quick guide to this TG2 site </span>
##          % else:
##              <span><a href="${tg.url('/')}">Home</a> Back to your Quickstart Home page </span>
##          % endif
##        </li>
##        <li><a href="http://www.turbogears.org/2.1/docs/">TG2 Documents</a> - Read everything in the Getting Started section</li>
##        <li><a href="http://docs.turbogears.org/1.0">TG1 docs</a> (still useful, although a lot has changed for TG2) </li>
##       <li><a href="http://groups.google.com/group/turbogears"> Join the TG Mail List</a> for general TG use/topics  </li>
##      </ul>
##  </div>
</%def>

<%def name="sidebar_bottom()">
##  <div id="sb_bottom" class="sidebar">
##      <h2>Developing TG2</h2>
##      <ul class="links">
##        <li><a href="http://trac.turbogears.org/query?status=new&amp;status=assigned&amp;status=reopened&amp;group=type&amp;milestone=2.1&amp;order=priority">TG2 Trac tickets</a> What's happening now in TG2 development</li>
##        <li><a href="http://trac.turbogears.org/timeline">TG Dev timeline</a> (recent ticket updates, svn checkins, wiki changes)</li>
##        <li><a href="http://svn.turbogears.org/trunk">TG2 SVN repository</a> For checking out a copy</li>
##        <li><a href="http://turbogears.org/2.1/docs/main/Contributing.html#installing-the-development-version-of-turbogears-2-from-source">Follow these instructions</a> For installing your copy</li>
##        <li><a href="http://trac.turbogears.org/browser/trunk">TG2 Trac's svn view</a> In case you need a quick look</li>
##        <li><a href="http://groups.google.com/group/turbogears-trunk"> Join the TG-Trunk Mail List</a> for TG2 discuss/dev </li>
##      </ul>
##  </div>
</%def>

<%def name="header()">
<a href="http://github.com/moschlar/SAUCE"><img style="position: absolute; top: 0; right: 0; border: 0; z-index: 16;" src="https://a248.e.akamai.net/assets.github.com/img/4c7dc970b89fd04b81c8e221ba88ff99a06c6b61/687474703a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f77686974655f6666666666662e706e67" alt="Fork me on GitHub"></a>
  <div id="header">
    <h1>${g.title}<br />
        <span class="subtitle">${g.subtitle}</span>
    </h1>
  </div>
</%def>
<%def name="footer()">
  <hr />
  <div class="fcenter">
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
##        <li>${h.html.tags.link_to('Assignments', tg.url('/assignments'), class_=('', 'active')[page=='assignments'])}</li>
    % if request.identity:
##        <li>${h.html.tags.link_to('Submissions', tg.url('/submissions'), class_=('', 'active')[page=='submissions'])}</li>
##        <li>${h.html.tags.link_to('Tests', tg.url('/tests'), class_=('', 'active')[page=='tests'])}</li>
    % endif
##        <li>${h.html.tags.link_to('Scores', tg.url('/scores'), class_=('', 'active')[page=='scores'])}</li>
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

<%def name="sidebar_left()">
% if event:
  <div id="sb_left" class="sidebar">
      <h2>${event.name}</h2>
      <ul class="links">
        <li>${h.link('Event', tg.url('/events/%d' % (event.id)))}</li>
        <li>${h.link('Assignments', tg.url('/events/%d/assignments' % (event.id)))}</li>
        <li>${h.link('Submissions', tg.url('/events/%d/submissions' % (event.id)))}</li>
        <li>${h.link('Scores', tg.url('/events/%d/scores' % (event.id)))}</li>
      </ul>
  </div>
% endif
</%def>

</html>
