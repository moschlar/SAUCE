<%inherit file="local:templates.master"/>
<%namespace file="local:templates.details" name="details" />
<%namespace file="local:templates.lists" name="lists" />

% if breadcrumbs:
  <%def name="body_class()">navbar_left</%def>
% endif

<%def name="title()">
  Submission
</%def>

<%def name="headers()">
  <script type="text/javascript">
    function highline(number) {
      var high = document.getElementsByClassName("hll");
      for (var i=0; i < high.length; ++i) {
        high[i].classList.remove("hll");
      }
      var line = document.getElementsByClassName("line-"+number);
      for (var j=0; j < line.length; ++j) {
        line[j].classList.add("hll");
      }
    }
  </script>
</%def>

<h2>Submission 
% if submission and hasattr(submission, 'id'):
  ${submission.id}
% endif
</h2>

${details.submission(submission, source)}

  ${c.form(c.options, child_args=c.child_args) | n}

##% if submission.judgement:
##  ${details.judgement(submission.judgement, corrected_source, diff)}
##% endif

% if compilation:
  ${details.compilation(compilation)}
% endif

% if submission.testruns:
  ${lists.testruns(submission.testruns)}
% endif

