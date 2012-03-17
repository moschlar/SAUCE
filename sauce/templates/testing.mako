<%inherit file="/base.mako" />

<%def name="head_tags()">
  <!-- add some head tags here -->
</%def>

<h1>SAUCE - System for AUtomated Code Evaluation</h1>

<h2>Testing controller</h2>

<pre>
${c.output}
</pre>
