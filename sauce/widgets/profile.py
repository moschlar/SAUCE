'''
Created on 14.04.2012

@author: moschlar
'''

from tw.forms import TableForm, SingleSelectField, TextField, SubmitButton, TextArea, Spacer, FileField, Label, HiddenField, PasswordField
from tw.forms.validators import Email, FieldsMatch, Schema

passwordValidator = Schema(chained_validators=(FieldsMatch('password_1',
                                                           'password_2',
                                                            messages={'invalidNoMatch':
                                                                 "Passwords do not match"}),))

class ProfileForm(TableForm):

    
    fields = [
              TextField('user_name', help_text=u'User name', disabled=True),
              TextField('display_name', help_text=u'Real name'),
              Spacer(),
              TextField('email_address', help_text=u'Email address', validator=Email),
              Spacer(),
              PasswordField('password_1', label_text=u'Password'),
              PasswordField('password_2', label_text=u'Password', help_text=u'Repeat'),
              ]
    
    #hover_help = True
    
    # Hide submit field
    # submit_text = None
    

profile_form = ProfileForm('profile_form', validator=passwordValidator)