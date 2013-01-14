<%inherit file="local:templates.master"/>

<%def name="title()">
  ${language} - Language
</%def>

<div class="page-header">
  <h1>${language}
    <small>Language</small>
  </h1>
</div>

<div class="row">
    <div class="offset2 span8 well">
    <h2>${language}</h2>
      <h3>Language</h3>
      <dl>
        <dt>Lexer name</dt>
          <dd>${language.lexer_name}</dd>
        <dt>Source file extension</dt>
          <dd><code>${language.extension_src or "None"}</code></dd>
        <dt>Binary file extension</dt>
          <dd><code>${language.extension_bin or "None"}</code></dd>
       </dl>
  </div>
</div>

<div class="row">
  % if language.compiler:
    <div class="offset2 span8 well">
      <h3>Compiler</h3>
      <dl>
        <dt>Name</dt>
          <dd>${language.compiler.name}</dd>
        <dt>Command line</dt>
          <dd><code>${language.compiler.path} ${language.compiler.argv}</code></dd>
        <dt>Timeout</dt>
          <dd>${'%.1f' % language.compiler.timeout}</dd>
        % if language.compiler.version_cmd:
          <dt>Version</dt>
            <dd>
            <dd>
##<code>${language.compiler.path} ${language.compiler.version_cmd}</code></dd>
<pre>${c.system("%s %s" % (language.compiler.path, language.compiler.version_cmd))}</pre>
            </dd>
        % endif
        % if language.compiler.help_cmd:
          <dt>Help</dt>
            <dd>
##<code>${language.compiler.path} ${language.compiler.help_cmd}</code></dd>
<pre>${c.system("%s %s" % (language.compiler.path, language.compiler.help_cmd))}</pre>
        % endif
      </dl>
    </div>
  % endif
  % if language.interpreter:
    <div class="offset2 span8 well">
      <h3>Interpreter</h3>
      <dl>
        <dt>Name</dt>
        <dd>${language.interpreter.name}</dd>
        <dt>Command line</dt>
        <dd><code>${language.interpreter.path} ${language.interpreter.argv}</code></dd>
        % if language.interpreter.version_cmd:
          <dt>Version</dt>
            <dd>
            <dd>
##<code>${language.interpreter.path} ${language.interpreter.version_cmd}</code></dd>
<pre>${c.system("%s %s" % (language.interpreter.path, language.interpreter.version_cmd))}</pre>
            </dd>
        % endif
        % if language.interpreter.help_cmd:
          <dt>Help</dt>
            <dd>
##<code>${language.interpreter.path} ${language.interpreter.help_cmd}</code></dd>
<pre>${c.system("%s %s" % (language.interpreter.path, language.interpreter.help_cmd))}</pre>
        % endif
      </dl>
    </div>
  % endif
</div>
