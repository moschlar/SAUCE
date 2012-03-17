<%
  if not hasattr(c, 'site'):
    c.site = ''
%>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>${c.site} - SAUCE</title>
##
% if hasattr(self, 'head_tags'):
    ${self.head_tags()}
% endif
##
    <!-- Le styles -->
    <link href="/bootstrap/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
    </style>
    <link href="/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">

    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

##    <!-- Le fav and touch icons -->
##    <link rel="shortcut icon" href="/bootstrap/ico/favicon.ico">
##    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/bootstrap/ico/apple-touch-icon-114-precomposed.png">
##    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/bootstrap/ico/apple-touch-icon-72-precomposed.png">
##    <link rel="apple-touch-icon-precomposed" href="/bootstrap/ico/apple-touch-icon-57-precomposed.png">
  </head>

  <body>

## Fork me on Github ribbon
<a href="https://github.com/moschlar/SAUCE"><img style="position: absolute; top: 0; right: 0; border: 0; z-index: 1050;" src="https://a248.e.akamai.net/assets.github.com/img/71eeaab9d563c2b3c590319b398dd35683265e85/687474703a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f677261795f3664366436642e706e67" alt="Fork me on GitHub"></a>

## NAVIGATION

    <div class="navbar navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="brand" href="${url(controller='')}">SAUCE</a>
          <div class="nav-collapse">
            <ul class="nav">
              <li class="${('', 'active')[c.site == 'Home']}">
                <a href="${url(controller='main', action='index')}">Home</a>
              </li>
              <li class="${('', 'active')[c.site == 'About']}">
                <a href="${url(controller='main', action='about')}">About</a>
              </li>
              <li class="${('', 'active')[c.site == 'Contact']}">
                <a href="${url(controller='main', action='contact')}">Contact</a>
              </li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

## END NAVIGATION


    <div class="container">

## FLASH

% if hasattr(c, 'messages'):
  % for msg in c.messages:
    <div class="flash ${msg.type}">${msg.msg}</div>
  % endfor
% endif

## END FLASH

${self.body()}

      <hr>

      <footer>
        <p>
          &copy; 2012 Moritz Schlarb and all other contributing developers<br />
          SAUCE is free software, released under the <a href="http://www.opensource.org/licenses/bsd-license.php">2-clause BSD license</a>.<br />
          See the <a href="https://github.com/moschlar/SAUCE">source code</a> with <a href="https://github.com/moschlar/SAUCE/blob/master/LICENSE.txt">licensing information</a> on Github.<br />
          Written in <a href="http://www.python.org">Python</a> using <a href="http://www.pylonsproject.org/projects/pylons-framework/about">Pylons</a>, <a href="http://www.sqlalchemy.org/">SQLAlchemy</a> and many other great free software products.
          </p>
      </footer>

    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/bootstrap/js/jquery.js"></script>
    <script src="/bootstrap/js/bootstrap-transition.js"></script>
    <script src="/bootstrap/js/bootstrap-alert.js"></script>
    <script src="/bootstrap/js/bootstrap-modal.js"></script>
    <script src="/bootstrap/js/bootstrap-dropdown.js"></script>
    <script src="/bootstrap/js/bootstrap-scrollspy.js"></script>
    <script src="/bootstrap/js/bootstrap-tab.js"></script>
    <script src="/bootstrap/js/bootstrap-tooltip.js"></script>
    <script src="/bootstrap/js/bootstrap-popover.js"></script>
    <script src="/bootstrap/js/bootstrap-button.js"></script>
    <script src="/bootstrap/js/bootstrap-collapse.js"></script>
    <script src="/bootstrap/js/bootstrap-carousel.js"></script>
    <script src="/bootstrap/js/bootstrap-typeahead.js"></script>

  </body>
</html>