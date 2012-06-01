# -*- coding: utf-8 -*-
'''
Created on 13.04.2012
Ported to tw2 on 25.05.2012

@author: moschlar
'''

import tw2.core as twc
import tw2.forms as twf
import tw2.dynforms as twdf
import tw2.bootstrap as twb
from sauce.widgets.lib import FloatValidator


class JudgementForm(twb.HorizontalForm, twdf.CustomisedTableForm):

    title = 'Judgement'

    assignment_id = twf.HiddenField()
    submission_id = twf.HiddenField()

    class annotations(twdf.GrowingGridLayout):
        line = twf.TextField(size=3, validator=twc.IntValidator, css_class='span1')
        comment = twf.TextField(size=65, css_class='span4')
    #Autosize('comment', help_text=u'Comment on the above source code'),
    comment = twf.TextArea(placeholder=u'Comment on the above source code', css_class='span5', rows=8)
    #Autosize('corrected_source', help_text=u'Paste your corrected source code here'),
    corrected_source = twf.TextArea(placeholder=u'Correct the above source code', css_class='span5', rows=8)
    grade = twf.TextField(placeholder=u'Grade this submission', validator=FloatValidator, css_class='span2')

    buttons = [
        #TODO: Distinguishable Buttons
        twb.SubmitButton('submit', name='submit', value='Submit', css_class='btn btn-primary'),
        twb.ResetButton('reset', name='reset', value='Delete', css_class='btn btn-danger')]

