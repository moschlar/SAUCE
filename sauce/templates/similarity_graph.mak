<%inherit file="local:templates.master" />

<%def name="title()">
  Similarity graph
</%def>

<%def name="headers()">
  <script type="text/javascript" src="/javascript/d3.v2.js"></script>
    <style type="text/css">
${c.style | n}
    </style>
</%def>

<div class="page-header">
  <h1>Similarity graph
  % if assignment:
    <small>Assignment ${assignment.id} - ${assignment.name}</small></h1>
  % endif
</div>


<div class="row">
<div class="span12">
<h2>${header}</h2>

<div id="chart"></div>

<script type="text/javascript">
${c.script | n}
</script>

</div>
</div>
