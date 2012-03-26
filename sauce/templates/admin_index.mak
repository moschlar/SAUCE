<%inherit file="local:templates.master"/>

<%def name="title()">
  Administration System
</%def>

<div style="height:0px;"> &nbsp; </div>
    <h2>${g.title} Admin</h2>
##    This is a fully-configurable administrative tool to help you administer your website.
##    Below is links to all of your models.<br/>    They will bring you to a listing of the objects
##    in your database.

<%
  model_grid = [
                ('News', ['NewsItem']),
                ('Events', ['Event', 'Course', 'Contest']),
                ('Languages', ['Compiler', 'Language', 'Interpreter']),
                ('Assignments', ['Assignment', 'Submission', 'Test', 'Testrun']),
                ('Participants', ['Student', 'Team', 'Teacher']),
                ('Authorization', ['User', 'Group', 'Permission'])
                ]
%>

<table class="admin_grid">
  % for (name, models) in model_grid:
    <tr>
    <th>${name}: </th>
    % for model in models:
      <td>
        <a href='${model.lower()}s/' class="edit_link">${model}</a>
      </td>
    % endfor
    </tr>
  % endfor
  <tr>
</table>
