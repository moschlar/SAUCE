'''
Created on 14.04.2012

@author: moschlar
'''

import tw2.core as twc
import tw2.bootstrap.forms as twbf
from formencode.validators import FieldsMatch


class ProfileForm(twbf.HorizontalForm):

    user_name = twbf.LabelField()
    last_name = twbf.TextField()
    first_name = twbf.TextField()

    email_address = twbf.TextField(validator=twc.EmailValidator)

    password_1 = twbf.PasswordField()
    password_2 = twbf.PasswordField()

    validator = FieldsMatch('password_1', 'password_2')
