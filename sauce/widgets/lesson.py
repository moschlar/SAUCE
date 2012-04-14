'''
Created on 15.04.2012

@author: moschlar
'''
from tw.api import WidgetsList
from tw.forms import TableForm, TextField, TextArea, Spacer, HiddenField, SubmitButton, PasswordField
from tw.dynforms import GrowingTableFieldSet, CustomisedForm
from tw.forms.validators import Email, FieldsMatch, Schema

passwordValidator = Schema(chained_validators=(FieldsMatch('password',
                                                           'password_verify',
                                                            messages={'invalidNoMatch':
                                                                 "Passwords do not match"}),))

class TeamForm(TableForm, CustomisedForm):
    
    class StudentForm(GrowingTableFieldSet):
        
        class children(WidgetsList):
            user_name = TextField()
            display_name = TextField()
            password = PasswordField()
            password_verify = PasswordField()
        
        validator = passwordValidator()
    
    fields = [
              TextField('name'),
              StudentForm('students', validator=passwordValidator)
              ]
    
team_form = TeamForm('team_form', validator=passwordValidator)