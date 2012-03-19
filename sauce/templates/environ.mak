<%inherit file="local:templates.master"/>

<%def name="title()">
  Learning TurboGears 2.1: Information about TG and WSGI
</%def>

${parent.sidebar_top()}
<h2>The WSGI nature of the framework</h2>
  <p>In this page you can see all the WSGI variables your request object has, 
     the ones in capital letters are required by the spec, then a sorted by
     component list of variables provided by the Components, and at last
     the "wsgi." namespace with very useful information about your WSGI Server</p>
   
  <h4>The keys in the environment are:</h4> 
  <table>
      %for key in sorted(environment):
      <tr>
          <td>${key}</td>
          <td>${environment[key]}</td>
      </tr>
      %endfor
  </table>
  
  <h4>args are: </h4>
  <table>
      %for item in args:
      <tr>
          <td>${item}</td>
      </tr>
      %endfor
  </table>
  
  <h4>kwargs are: </h4>
  <table>
      %for key in sorted(kwargs):
      <tr>
          <td>${key}</td>
          <td>${kwargs[key]}</td>
      </tr>
      %endfor
  </table>
  
  % if request.identity:
    <h4>keys in identity are: </h4>
    <table>
        %for key in sorted(request.identity):
        <tr>
            <td>${key}</td>
            <td>${request.identity[key]}</td>
        </tr>
        %endfor
    </table>
  % endif
  
<%def name="sidebar_bottom()"></%def>
