# -*- coding: utf-8 -*-
'''Judgement widget for SAUCE

@see: :mod:`tw2.core`

@since: 13.04.2012
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
import tw2.bootstrap.wysihtml5 as twbw

from sauce.widgets.lib import FloatValidator
from sauce.widgets.widgets import Wysihtml5, SmallTextField

try:
    from tw2.ace import AceWidget as SourceEditor
#    from tw2.codemirror import CodeMirrorWidget as SourceEditor
except ImportError:  # pragma: no cover
    from tw2.bootstrap.forms import TextArea as SourceEditor


class JudgementForm(twbf.HorizontalForm, twdf.CustomisedTableForm):

    title = 'Judgement'

    assignment_id = twbf.HiddenField(validator=twc.IntValidator)
    submission_id = twbf.HiddenField(validator=twc.IntValidator)

    class annotations(twdf.GrowingGridLayout):
        line = twbf.TextField(validator=twc.IntValidator, css_class='span1')
        comment = twbf.TextField(validator=twc.StringLengthValidator, css_class='span6')
    comment = Wysihtml5(
        placeholder=u'Comment on the above source code',
        validator=twc.StringLengthValidator,
        rows=6,
        parser=True,
    )
    corrected_source = SourceEditor(
        placeholder=u'Correct the above source code',
        help_text=u'It is currently not possible for you to run the test cases '
        'with this corrected source code. Sorry!',
        validator=twc.StringLengthValidator,
        css_class='span8', cols=80, rows=24)
    grade = SmallTextField(
        placeholder=u'Grade this submission',
        validator=FloatValidator,
    )

    def prepare(self):
        self.safe_modify('source')
        try:
            self.child.c.corrected_source.mode = self.value.submission.language.lexer_name
        except AttributeError:
            pass
        super(JudgementForm, self).prepare()
