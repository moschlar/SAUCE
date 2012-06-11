'''
Created on 14.04.2012

@author: moschlar
'''

import tw2.core as twc
import tw2.bootstrap as twb
from formencode.validators import FieldsMatch


class ProfileForm(twb.HorizontalForm):

    user_name = twb.TextField()
    last_name = twb.TextField()
    first_name = twb.TextField()

    email_address = twb.TextField(validator=twc.EmailValidator)

    password_1 = twb.PasswordField()
    password_2 = twb.PasswordField()

    validator = FieldsMatch('password_1', 'password_2')
