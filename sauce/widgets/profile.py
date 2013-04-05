'''
Created on 14.04.2012

@author: moschlar
'''
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import tw2.core as twc
import tw2.bootstrap.forms as twbf
from formencode.validators import FieldsMatch


class ProfileForm(twbf.HorizontalForm):

    user_name = twbf.LabelField()
    display_name = twbf.TextField()
    last_name = twbf.TextField()
    first_name = twbf.TextField()

    email_address = twbf.TextField(validator=twc.EmailValidator)

    password_l = twbf.Label(text='Only if you want to change your password:', validator=twc.BlankValidator)
    password_1 = twbf.PasswordField(label='New password')
    password_2 = twbf.PasswordField(label='Repeat password')

    validator = FieldsMatch('password_1', 'password_2')
