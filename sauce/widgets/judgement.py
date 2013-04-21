# -*- coding: utf-8 -*-
'''
Created on 13.04.2012
Ported to tw2 on 25.05.2012

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
import tw2.dynforms as twdf
import tw2.bootstrap.forms as twbf
import tw2.tinymce as twt
from sauce.widgets.lib import FloatValidator

try:
    from tw2.ace import AceWidget as SourceEditor
#    from tw2.codemirror import CodeMirrorWidget as SourceEditor
except ImportError:
    from tw2.bootstrap.forms import TextArea as SourceEditor


class JudgementForm(twbf.HorizontalForm, twdf.CustomisedTableForm):

    title = 'Judgement'

    assignment_id = twbf.HiddenField(validator=twc.IntValidator)
    submission_id = twbf.HiddenField(validator=twc.IntValidator)

    class annotations(twdf.GrowingGridLayout):
        line = twbf.TextField(validator=twc.IntValidator, css_class='span1')
        comment = twbf.TextField(css_class='span6')
    #Autosize('comment', help_text=u'Comment on the above source code'),
    comment = twt.TinyMCEWidget(placeholder=u'Comment on the above source code',
        css_class='span7', rows=6)
    #Autosize('corrected_source', help_text=u'Paste your corrected source code here'),
    corrected_source = SourceEditor(placeholder=u'Correct the above source code',
        help_text=u'It is currently not possible for you to run the test cases '
        'with this corrected source code. Sorry!',
        css_class='span8', cols=80, rows=24)
    grade = twbf.TextField(placeholder=u'Grade this submission',
        validator=FloatValidator, css_class='span3')

    def prepare(self):
        self.safe_modify('source')
        try:
            self.child.c.corrected_source.mode = self.value.submission.language.lexer_name
        except AttributeError:
            pass
        super(JudgementForm, self).prepare()
