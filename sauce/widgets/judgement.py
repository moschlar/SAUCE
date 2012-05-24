# -*- coding: utf-8 -*-
'''
Created on 13.04.2012

@author: moschlar
'''

import tw2.core as twc
import tw2.forms as twf
import tw2.dynforms as twdf

#from tw.api import WidgetsList
#from tw.forms import TableForm, TextField, TextArea, Spacer, HiddenField, SubmitButton
#
#from tw.dynforms import GrowingTableFieldSet, CustomisedForm
#from tw.forms.validators import Int, Number
#from tw.dynforms.widgets import StripDictValidator
#from tw.autosize.widgets import Autosize

class JudgementForm(twdf.CustomisedTableForm):
    #show_errors = True
    title = 'Judgement'
    action = 'post_judge'
    
    assignment_id = twf.HiddenField()
    submission_id = twf.HiddenField()
    class annotations(twdf.GrowingGridLayout):
        
        line = twf.TextField(size=3, validator=twc.IntValidator)
        comment = twf.TextField(size=65)
        
        #validator = StripDictValidator('grow', if_missing=[])
    #Autosize('comment', help_text=u'Comment on the above source code'),
    comment = twf.TextArea(placeholder=u'Comment on the above source code', help_text=u'Comment on the above source code')
    #Autosize('corrected_source', help_text=u'Paste your corrected source code here'),
    corrected_source = twf.TextArea(placeholder=u'Paste your corrected source code here', help_text=u'Paste your corrected source code here')
    grade = twf.TextField(placeholder=u'Grade this submission')
    
    #hover_help = True
    
    #submit = twf.SubmitButton(class_="btn")
    
    # Hide submit field
    #submit_text = None

