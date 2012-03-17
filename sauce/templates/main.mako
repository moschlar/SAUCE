<%inherit file="/base.mako" />

<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>

<h1>System for AUtomated Code Evaluation</h1>
<h2>${c.site}</h2>

<p>This project is currently under heavy development.</p>

<h3>Development feature testing list</h3>
<p>
  This list provides some links to functionality currently
  being worked on to ease in testing.
</p>

<ul>
  <li><a href="${url(controller='testing', action='runner')}">Runner</a></li>
</ul>