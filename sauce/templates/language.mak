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
      ##<h2>${language}</h2>
      <h3>Language</h3>
      <dl>
        <dt>Lexer name</dt>
          <dd><code>${language.lexer_name}</code></dd>
        <dt>Source file extension</dt>
          <dd>
            % if language.extension_src:
              <code>${language.extension_src}</code>
            % else:
              None
            % endif
          </dd>
        <dt>Binary file extension</dt>
          <dd>
            % if language.extension_bin:
              <code>${language.extension_bin}</code>
            % else:
              None
            % endif
          </dd>
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
        % if language.compiler.version:
          <dt>Version</dt>
            <dd><pre>${language.compiler.version}</pre></dd>
        % endif
        % if language.compiler.help:
          <dt>Help</dt>
            <dd><pre>${language.compiler.help}</pre></dd>
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
        % if language.interpreter.version:
          <dt>Version</dt>
            <dd>
            <dd><pre>${language.interpreter.version}</pre></dd>
        % endif
        % if language.interpreter.help:
          <dt>Help</dt>
            <dd><pre>${language.interpreter.help}</pre></dd>
        % endif
      </dl>
    </div>
  % endif
</div>
