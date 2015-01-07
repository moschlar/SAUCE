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
import tw2.jquery as twj
import tw2.dynforms as twdf
import tw2.bootstrap.forms as twbf

from sauce.widgets.lib import ays_js
from sauce.widgets.widgets import SmallTextField, LargeSourceEditor, AdvancedWysihtml5
from sauce.widgets.validators import FloatValidator, BleachValidator


class JudgementForm(twbf.HorizontalForm, twdf.CustomisedTableForm):

    title = 'Judgement'

    assignment_id = twbf.HiddenField(validator=twc.IntValidator)
    submission_id = twbf.HiddenField(validator=twc.IntValidator)

    class annotations(twdf.GrowingGridLayout):
        line = twbf.TextField(validator=twc.IntValidator, css_class='span1')
        comment = twbf.TextField(validator=twc.StringLengthValidator, css_class='span6')

    comment = AdvancedWysihtml5(
        placeholder=u'Comment on the above source code',
    )
    corrected_source = LargeSourceEditor(
        placeholder=u'Correct the above source code',
        help_text=u'It is currently not possible for you to run the test cases '
            'with this corrected source code. Sorry!',
        validator=twc.StringLengthValidator(strip=False),
        fullscreen=True,
    )
    grade = SmallTextField(
        placeholder=u'Grade this submission',
        validator=FloatValidator,
    )

    buttons = [
        twbf.SubmitButton('save_draft', name='save_draft', value='Save as draft', css_class='btn'),
        twbf.SubmitButton('save_publish', name='save_publish', value='Save and publish'),
    ]

    @classmethod
    def post_define(cls):
        if ays_js not in cls.resources:
            cls.resources.append(ays_js)

    @classmethod
    def validate(cls, params, state=None):
        result = super(JudgementForm, cls).validate(params, state=state)

        # Preserve which button was clicked
        save_draft = params.get('save_draft', None)
        save_publish = params.get('save_publish', None)
        if save_draft and save_publish:
            raise twc.validation.ValidationError('save_draft and save_publish')
        elif save_draft:
            result['public'] = False
        elif save_publish:
            result['public'] = True

        return result

    def prepare(self):
        self.safe_modify('source')
        try:
            self.child.c.corrected_source.mode = self.value.submission.language.lexer_name
        except AttributeError:
            pass

        super(JudgementForm, self).prepare()

        # TODO: Are-you-sure hook for Wysihtml5
        self.add_call(twj.jQuery(twc.js_symbol('document')).ready(twc.js_symbol(u'''\
function () {
    $("%(form)s").areYouSure();
    $("%(corrected_source)s + .CodeMirror")[0].CodeMirror.on('changes', function(instance) { instance.save(); });
}''' % {'form': self.selector or 'Form', 'corrected_source': self.child.c.corrected_source.selector})))
