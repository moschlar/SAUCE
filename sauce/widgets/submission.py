# -*- coding: utf-8 -*-
'''
Created on 17.03.2012

@author: moschlar
'''

from tw.forms import TableForm, SingleSelectField, TextField, SubmitButton, TextArea, Spacer, FileField, Label, HiddenField

class SubmissionForm(TableForm):
    
    language_options = [x for x in enumerate((u'Brainfuck', ))]
    
    class ButtonTable(TableForm):
        
        params = dict(cols='Columns')
        
        template = u'''
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
                           help_text=u'Compile and run tests on your source code'), 
                  SubmitButton('submit', disabled=False, label_text='Submit', default='Submit', named_button=True, 
                           help_text=u'Submit your source code for final evaluation'),
                  SubmitButton('reset', label_text='Reset', default='Reset', named_button=True, 
                           help_text=u'Reset this submission'),
                  ]
        cols = len(fields)
    
    fields = [
              HiddenField('assignment_id'), HiddenField('submission_id'),
              TextField('filename', help_text=u'Filename (e.g. Classname.java for java programs)'),
              TextArea('source', help_text=u'Paste your source code here'),
              Label(text='OR'),
              FileField('source_file', help_text=u'Upload your source code file here'),
              Spacer(),
              SingleSelectField('language_id', options=language_options, label_text='Language', help_text=u'Select the programming language for the source code'),
              Spacer(),
              ButtonTable('buttons', label_text=u''),
              Spacer(),
              ]
    
    #hover_help = True
    
    # Hide submit field
    submit_text = None
    

submission_form = SubmissionForm('submission_form')