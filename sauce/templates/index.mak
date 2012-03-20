<%inherit file="local:templates.master"/>

<%def name="title()">
  Welcome to the System for AUtomated Code Evaluation
</%def>

${parent.sidebar_top()}

##<div id="getting_started">
  <h2>SAUCE</h2>
  <h3>System for AUtomated Code Evaluation</h3>
  <p>Welcome to SAUCE.<br />
  This project is currently under heavy development.</p>
  
##  <p>TurboGears 2 is rapid web application development toolkit designed to make your life easier.</p>
##  <ol id="getting_started_steps">
##    <li class="getting_started">
##      <h3>Code your data model</h3>
##      <p> Design your data model, Create the database, and Add some bootstrap data.</p>
##    </li>
##    <li class="getting_started">
##      <h3>Design your URL architecture</h3>
##      <p> Decide your URLs, Program your controller methods, Design your 
##          templates, and place some static files (CSS and/or JavaScript). </p>
##    </li>
##    <li class="getting_started">
##      <h3>Distribute your app</h3>
##      <p> Test your source, Generate project documents, Build a distribution.</p>
##    </li>
##  </ol>
##</div>
<div class="clearingdiv" />
##<div class="notice"> Thank you for choosing TurboGears. 
##</div>

<%def name="sidebar_bottom()"><p>Test</p></%def>
