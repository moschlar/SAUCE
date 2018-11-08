## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

<%inherit file="local:templates.master"/>

<%def name="title()">
  ${language} - Language
</%def>

<div class="page-header">
  <h1>${language.name}
    <small>Language</small>
  </h1>
</div>

<div class="row">
    <div class="span8 well">
      ##<h2>${language.name}</h2>
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
    <div class="span8 well">
      <h3>Compiler</h3>
      <dl>
        <dt>Name</dt>
          <dd>${language.compiler.name}</dd>
        <dt>Command line</dt>
          <dd><code>${language.compiler.path} ${language.compiler.argv}</code></dd>
        % if language.compiler.timeout:
          <dt>Timeout</dt>
            <dd>${'%.1f' % language.compiler.timeout}</dd>
        % endif
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
    <div class="span8 well">
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
