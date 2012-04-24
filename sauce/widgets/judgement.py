# -*- coding: utf-8 -*-
'''
Created on 13.04.2012

@author: moschlar
'''

from sauce.widgets.lib import ButtonTable

from tw.api import WidgetsList
from tw.forms import TableForm, TextField, TextArea, Spacer, HiddenField, SubmitButton

from tw.dynforms import GrowingTableFieldSet, CustomisedForm
from tw.forms.validators import Int, Number
from tw.dynforms.widgets import StripDictValidator

class JudgementForm(TableForm, CustomisedForm):
    #show_errors = True
    
#    class SubmitButtonTable(ButtonTable):
#        
#        fields = [
#                  SubmitButton('test', label_text='Test', default='Test', named_button=True, 
#                           help_text=u'Compile and run tests on your source code'), 
#                  SubmitButton('submit', disabled=False, label_text='Submit', default='Submit', named_button=True, 
#                           help_text=u'Submit your source code for final evaluation'),
#                  SubmitButton('reset', label_text='Reset', default='Reset', named_button=True, 
#                           help_text=u'Reset this submission'),
#                  ]
#        cols = len(fields)
#        #validator = None
    
    class AnnotationForm(GrowingTableFieldSet):
        
        class children(WidgetsList):
            line = TextField(size=3, validator=Int)
            comment = TextField(size=65)
        
        #validator = StripDictValidator('grow', if_missing=[])
    
    fields = [
              HiddenField('assignment_id'), HiddenField('submission_id'),
              AnnotationForm('annotations', help_text=u'New lines are automatically appended'),
              Spacer(),
              TextArea('comment', help_text=u'Comment on the above source code'),
              Spacer(),
              TextArea('corrected_source', help_text=u'Paste your corrected source code here'),
              Spacer(),
              TextField('grade'),
              Spacer(),
#              SubmitButtonTable('buttons', label_text=u''),
#              Spacer(),
              ]
    
    #hover_help = True
    
    # Hide submit field
    #submit_text = None


judgement_form = JudgementForm('judgement_form')