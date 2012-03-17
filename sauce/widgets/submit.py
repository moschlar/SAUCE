'''
Created on 17.03.2012

@author: moschlar
'''
from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea, Spacer, FileField, Label, HiddenField, CheckBox


class SubmitForm(TableForm):
    
    language_options = [x for x in enumerate(('Brainfuck'))]
    
    fields = [
              HiddenField('assignment'),
              TextArea('source', help_text='Paste your source code here'),
              Label('or', text='OR'),
              FileField('source_file', help_text = 'Upload your source code file here'),
              Spacer(),
              SingleSelectField('language', options=language_options, help_text='Select the programming language for the source code'),
              Spacer(),
              CheckBox('test', help_text= 'Automatically run tests on submission'),
              Spacer(),
              ]
    
    #hover_help = True
    
    submit_text = 'Submit source code'

submit_form = SubmitForm("submit_form")