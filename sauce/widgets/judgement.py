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
import tw2.tinymce as twt
from sauce.widgets.lib import FloatValidator


class JudgementForm(twb.HorizontalForm, twdf.CustomisedTableForm):

    title = 'Judgement'

    assignment_id = twf.HiddenField(validator=twc.IntValidator)
    submission_id = twf.HiddenField(validator=twc.IntValidator)

    class annotations(twdf.GrowingGridLayout):
        line = twf.TextField(validator=twc.IntValidator, css_class='span1')
        comment = twf.TextField(css_class='span6')
    #Autosize('comment', help_text=u'Comment on the above source code'),
    comment = twt.TinyMCEWidget(placeholder=u'Comment on the above source code',
        css_class='span7', rows=6)
    #Autosize('corrected_source', help_text=u'Paste your corrected source code here'),
    corrected_source = twf.TextArea(placeholder=u'Correct the above source code',
        help_text=u'It is currently not possible for you to run the test cases '\
        'with this corrected source code. Sorry!', css_class='span7', rows=10)
    grade = twf.TextField(placeholder=u'Grade this submission',
        validator=FloatValidator, css_class='span3')
