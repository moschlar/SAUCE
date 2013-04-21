# -*- coding: utf-8 -*-
'''
Created on 17.03.2012

@author: moschlar
'''
#
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
#

import tw2.core as twc
import tw2.bootstrap.forms as twbf

try:
    from tw2.ace import AceWidget as SourceEditor
#    from tw2.codemirror import CodeMirrorWidget as SourceEditor
except ImportError:
    from tw2.bootstrap.forms import TextArea as SourceEditor

try:
    from tw2.jqplugins.chosen import ChosenSingleSelectField as SingleSelectField
except ImportError:
    from tw2.forms.bootstrap import SingleSelectField


class SubmissionForm(twbf.HorizontalForm):

    title = 'Submission'

    id = twbf.HiddenField(validator=twc.IntValidator)
    assignment_id = twbf.HiddenField(validator=twc.IntValidator)

    filename = twbf.TextField(placeholder=u'Enter a filename, if needed',
        help_text=u'An automatically generated filename may not meet the '\
        'language\'s requirements (e.g. the Java class name)',
        css_class='span3')
    source = SourceEditor(placeholder=u'Paste your source code here',
        css_class='span8', cols=80, rows=24)
    source_file = twbf.FileField(css_class='span7')

    language_id = SingleSelectField(options=[], prompt_text=None,
        css_class='span3',
        required=True, validator=twc.IntValidator(required=True))

    def prepare(self):
        self.safe_modify('language_id')
        self.child.c.language_id.options = [(l.id, l.name) for l in self.value.assignment.allowed_languages]
        try:
            self.safe_modify('source')
            self.child.c.source.mode = self.value.language.lexer_name
        except AttributeError:
            pass
        super(SubmissionForm, self).prepare()
