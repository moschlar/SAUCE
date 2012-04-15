# -*- coding: utf-8 -*-
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
        validator = passwordValidator
        
        class children(WidgetsList):
            user_name = TextField(size=5)
            display_name = TextField(size=15)
            email_address = TextField(size=15)
            password = PasswordField(size=10)
            password_verify = PasswordField(size=10)
        
    
    fields = [
              TextField('name'),
              StudentForm('students')
              ]
    
team_form = TeamForm('team_form', validator=passwordValidator)