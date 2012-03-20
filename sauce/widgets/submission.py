'''
Created on 17.03.2012

@author: moschlar
'''
from tw.api import WidgetsList
from tw.forms import (TableForm, CalendarDatePicker, SingleSelectField, TextField, SubmitButton, Button, 
                      TextArea, Spacer, FileField, Label, HiddenField, CheckBox, TableMixin)


class SubmissionForm(TableForm):
    
    language_options = [x for x in enumerate(('Brainfuck', ))]
    
    class ButtonTable(TableForm):
        
        params = dict(cols='Columns')
        
        template = '''
<table>
  % for i, child in enumerate(children):
    % if (i % cols) == 0:
      <tr>
    % endif
      <td>${display_child(child)}</td>
    % if (i % cols) == cols-1:
      </tr>
    % endif
  % endfor
</table>
'''
        engine = 'mako'
        
        fields = [
                  SubmitButton('test', label_text='Test', default='Test', named_button=True, 
                           help_text='Compile and run tests on your source code'), 
                  SubmitButton('submit', disabled=False, label_text='Submit', default='Submit', named_button=True, 
                           help_text='Submit your source code for final evaluation'),
                  SubmitButton('reset', label_text='Reset', default='Reset', named_button=True, 
                           help_text='Reset this submission'),
                  ]
        cols = len(fields)
    
    fields = [
              HiddenField('assignment_id'), HiddenField('submission_id'),
              TextField('filename', help_text='Filename (e.g. Classname.java for java programs)'),
              TextArea('source', help_text='Paste your source code here'),
              Label(text='OR'),
              FileField('source_file', help_text = 'Upload your source code file here'),
              Spacer(),
              SingleSelectField('language_id', options=language_options, label_text='Language', help_text='Select the programming language for the source code'),
              Spacer(),
              #CheckBox('autotest', help_text= 'Automatically run tests on submission'),
              ButtonTable('buttons', label_text=''),
              Spacer(),
              ]
    
    #hover_help = True
    
    # Hide submit field
    submit_text = None

submission_form = SubmissionForm('submission_form')