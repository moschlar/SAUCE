<%inherit file="local:templates.master"/>

<%def name="title()">
  Documentation - Tests
</%def>

<p><a href=".">Back to Test Admin</a></p>

<h1 class="title">Test configuration</h1>

<p>Specifying the correct test parameters is probably the most important and difficult task for a teacher user.</p>
<p>Therefore, this documentation seeks to explain <strong>how</strong> the tests work and <strong>how</strong> to correctly configure them.</p>
<div class="section" id="how-tests-work">
<h1>How tests work</h1>
<p>Basically, there are two types of <em>Tests</em> and two types of <em>Testruns</em>.</p>
<p>A <em>Test</em> has a boolean attribute <tt class="docutils literal">visible</tt>.</p>
<blockquote>
Only if <tt class="docutils literal">visible</tt> is set to <tt class="docutils literal">True</tt>, the test input and the expected test output are shown to the user on the <em>Assignment</em> page.</blockquote>
<p>Different types of <em>Testruns</em> are performed when different buttons are clicked on the <em>Submission</em> page:</p>
<ul class="simple">
<li><em>Testruns</em> performed after clicking Test are not saved to the database, their output is only once rendered for the submitter while editing his <em>Submission</em>.</li>
<li><em>Testruns</em> performed after clicking Submit are saved to the database and available for later displaying.</li>
</ul>
<div class="section" id="the-buttons-on-the-submission-page">
<h2>The buttons on the <em>Submission</em> page</h2>
<p>On the <em>Submission</em> edit page, there are three buttons:
Test, Submit and Reset (the Submit button will be disabled initially).
Their functionality explained in detail:</p>
<dl class="docutils">
<dt><strong>Test</strong></dt>
<dd><p class="first">When the <em>User</em> has entered his <em>Submission</em> source code or selected a file to upload and clicks on the Test button, the <em>Submission</em> is saved to the database and all visible <em>Tests</em> associated with the <em>Assignment</em> are run.</p>
<p>For each test, the test input, expected and observed output and error output (if any) are displayed (for convenience, a diff is displayed when the test run was not successful).</p>
<p class="last">Only if all visible <em>Tests</em> ran successfully, the Submit button is enabled.</p>
</dd>
<dt><strong>Submit</strong></dt>
<dd><p class="first">When the <em>User</em> clicks the Submit button, the <em>Submission</em> is marked as <tt class="docutils literal">completed</tt> and cannot be edited anymore. Then all <em>Test</em> cases (visible and non-visible) are run on the <em>Submission</em> and their respective output and error data as well as their result after validation get saved to the database for future displaying.</p>
<p class="last">The Submit button is only enabled, when the <em>User</em> has previously tested his submission successfully. While this prevents <em>Student</em>, <em>Teacher</em> and the system from running lots of presumably failing <em>Test</em> cases on the <em>Submission</em>, it still ensures that the <em>Submission</em> source code is safely stored to the database and the <em>Teacher</em> can see and grade the failed attempt.
Also, the <em>Teacher</em> can override this convention and run the non-visible <em>Tests</em> to see if the <em>Submission</em> is just missing some corner-cases.</p>
</dd>
<dt><strong>Reset</strong></dt>
<dd>When the Reset button is clicked, the <em>Submission</em> is deleted from the database. The <em>User</em> gets redirected to the corresponding <em>Assignment</em> page of the <em>Submission</em> he just deleted.</dd>
</dl>
</div>
</div>
<div class="section" id="how-to-configure-tests">
<h1>How to configure tests</h1>
<p>When configuring a <em>Test</em> case there are many options available in the administration panel:</p>
<div class="section" id="running-options">
<h2>Running options</h2>
<table border="1" class="docutils">
<colgroup>
<col width="37%" />
<col width="15%" />
<col width="49%" />
</colgroup>
<thead valign="bottom">
<tr><th class="head">Option</th>
<th class="head">Type /
Default</th>
<th class="head">Description</th>
</tr>
</thead>
<tbody valign="top">
<tr><td><tt class="docutils literal">visible</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">False</tt></p>
</td>
<td>If set, the <em>Test</em> is shown to
users on the <em>Assignment</em> page
and it is run when the Test
button is clicked.</td>
</tr>
<tr><td><tt class="docutils literal">timeout</tt></td>
<td><p class="first">Float</p>
<p class="last">None</p>
</td>
<td><p class="first">Maximum runtime of test process.</p>
<p class="last">If not set, the value from the
<em>Assignment</em> will be used or no
time limit at all is applied.</p>
</td>
</tr>
<tr><td><tt class="docutils literal">argv</tt></td>
<td><p class="first">String</p>
<p class="last">None</p>
</td>
<td><p class="first">Command line arguments for test
program run</p>
<p>Possible variables are:</p>
<table class="last docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field"><th class="field-name"><tt class="docutils literal">{path}</tt>:</th><td class="field-body">Absolute path to
temporary working directory</td>
</tr>
<tr class="field"><th class="field-name"><tt class="docutils literal">{infile}</tt>:</th><td class="field-body">Full path to test
input file</td>
</tr>
<tr class="field"><th class="field-name"><tt class="docutils literal">{outfile}</tt>:</th><td class="field-body">Full path to test
output file</td>
</tr>
</tbody>
</table>
</td>
</tr>
<tr><td><tt class="docutils literal">input_type</tt> /
<tt class="docutils literal">output_type</tt></td>
<td><p class="first">Enum</p>
<p class="last"><tt class="docutils literal">stdin</tt>/
<tt class="docutils literal">stdout</tt></p>
</td>
<td>If set, any line starting with
<tt class="docutils literal">comment_prefix</tt> will be
ignored in the test validation</td>
</tr>
<tr><td><tt class="docutils literal">input_filename</tt> /
<tt class="docutils literal">output_filename</tt></td>
<td><p class="first">String</p>
<p class="last">None</p>
</td>
<td>If set, any line starting with
<tt class="docutils literal">comment_prefix</tt> will be
ignored in the test validation</td>
</tr>
<tr><td><tt class="docutils literal">input_data</tt> /
<tt class="docutils literal">output_data</tt></td>
<td>String</td>
<td>If set, any line starting with
<tt class="docutils literal">comment_prefix</tt> will be
ignored in the test validation</td>
</tr>
</tbody>
</table>
</div>
<div class="section" id="validation-options">
<h2>Validation options</h2>
<table border="1" class="docutils">
<colgroup>
<col width="37%" />
<col width="15%" />
<col width="49%" />
</colgroup>
<thead valign="bottom">
<tr><th class="head">Option</th>
<th class="head">Type /
Default</th>
<th class="head">Description</th>
</tr>
</thead>
<tbody valign="top">
<tr><td><tt class="docutils literal">ignore_case</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">True</tt></p>
</td>
<td>To ignore the case of the
output, this simply calls
<tt class="docutils literal">.lower()</tt> on the whole
output string before comparison</td>
</tr>
<tr><td><tt class="docutils literal">ignore_returncode</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">True</tt></p>
</td>
<td>If <tt class="docutils literal">False</tt>, the <em>Test</em> will
only be considered successful,
if its process return code is
<tt class="docutils literal">== 0</tt></td>
</tr>
<tr><td><tt class="docutils literal">comment_prefix</tt></td>
<td><p class="first">String</p>
<p class="last"><tt class="docutils literal">'#'</tt></p>
</td>
<td>If set, any line starting with
<tt class="docutils literal">comment_prefix</tt> will be
ignored in the test validation</td>
</tr>
<tr><td><tt class="docutils literal">show_partial_match</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">True</tt></p>
</td>
<td>If set, if the observed output
matches the beginning of the
expected output, this partial
match will be displayed as such
to the <em>User</em> to indicate a
possible timeout error.</td>
</tr>
<tr><td><tt class="docutils literal">separator</tt></td>
<td><p class="first">String</p>
<p class="last"><tt class="docutils literal">None</tt></p>
</td>
<td><p class="first">The separator string to use for
<tt class="docutils literal">.split()</tt>, if set.
May contain a string as set of
characters on any of which the
output shall be splitted.</p>
<p class="last">If set to <tt class="docutils literal">None</tt> (default),
splitting will be done on any
whitespace character
(Python default).</p>
</td>
</tr>
<tr><td><tt class="docutils literal">splitlines</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">False</tt></p>
</td>
<td>Split output by lines using the
Python <tt class="docutils literal">.splitlines()</tt>
function.</td>
</tr>
<tr><td><tt class="docutils literal">split</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">True</tt></p>
</td>
<td><p class="first">Split output by <tt class="docutils literal">separator</tt>.</p>
<p class="last">Applies to full output, if
<tt class="docutils literal">splitlines</tt> is <tt class="docutils literal">False</tt>,
but to each line from
<tt class="docutils literal">.splitlines()</tt> if
<tt class="docutils literal">splitlines</tt> is <tt class="docutils literal">True</tt>.</p>
</td>
</tr>
<tr><td><tt class="docutils literal">sort</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">False</tt></p>
</td>
<td><p class="first">Sort output before comparison.</p>
<p>Parsing is performed first,
if enabled.</p>
<p>Results depends on
whether <tt class="docutils literal">splitlines</tt> and/or
<tt class="docutils literal">split</tt> are set:</p>
<p>if <tt class="docutils literal">split</tt> and <tt class="docutils literal">splitlines</tt>:
2-dimensional array in which
only the second dimension is
sorted (e.g.
<tt class="docutils literal">[[3, 4], [1, <span class="pre">2]])</span></tt></p>
<p class="last">if only <tt class="docutils literal">split</tt> or only
<tt class="docutils literal">splitlines</tt>:
1-dimensional list is sorted
by the types default comparator</p>
</td>
</tr>
<tr><td><tt class="docutils literal">parse_int</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">False</tt></p>
</td>
<td>Parse every substring in output
to <tt class="docutils literal">int</tt> before comparison.</td>
</tr>
<tr><td><tt class="docutils literal">parse_float</tt></td>
<td><p class="first">Boolean</p>
<p class="last"><tt class="docutils literal">False</tt></p>
</td>
<td>Parse every substring in output
to <tt class="docutils literal">float</tt> before comparison.</td>
</tr>
<tr><td><tt class="docutils literal">float_precision</tt></td>
<td><p class="first">Float</p>
<p class="last"><tt class="docutils literal">None</tt></p>
</td>
<td>The precision (number of
decimal digits) to compare
for floats</td>
</tr>
</tbody>
</table>
</div>
</div>
##</div>

