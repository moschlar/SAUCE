<%inherit file="local:templates.master"/>

<%def name="title()">Login</%def>

<div class="page-header">
  <h1>Login</h1>
</div>

<div class="row">
  <div class="span4 offset4">
    <form action="${tg.url('/login_handler', params=dict(came_from=came_from.encode('utf-8'), __logins=login_counter.encode('utf-8')))}" method="POST" class="well">
      <label for="login">Username:</label>
      <input type="text" id="login" name="login" class="span3" />
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" class="span3" />
      <label id="labelremember" for="loginremember" class="checkbox">
        <input type="checkbox" id="loginremember" name="remember" value="2252000" />
        Remember me
      </label>
      <button type="submit" class="btn btn-primary" id="submit" value="Login">Login</button>
    </form>
  </div>
</div>

