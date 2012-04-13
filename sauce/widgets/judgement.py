# -*- coding: utf-8 -*-
'''
Created on 13.04.2012

@author: moschlar
'''

from tw.api import WidgetsList
from tw.forms import TableForm, TextField, TextArea, Spacer, HiddenField

from tw.dynforms import GrowingTableFieldSet, CustomisedForm
from tw.forms.validators import Int

class JudgementForm(TableForm, CustomisedForm):
    show_errors = True

    class AnnotationForm(GrowingTableFieldSet):
        
        class children(WidgetsList):
            line = TextField(size=3, validator=Int())
            comment = TextField(size=65)
    
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
              ]
    
    #hover_help = True
    
    # Hide submit field
    #submit_text = None


judgement_form = JudgementForm('judgement_form')