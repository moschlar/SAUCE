# -*- coding: utf-8 -*-
'''User profile form

@see: :mod:`tw2.core`

@since: 14.04.2012
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

from sauce.widgets.widgets import MediumTextField, MediumMixin


class MediumLabelField(MediumMixin, twbf.LabelField):
    css_class = twbf.LabelField.css_class + ' ' + MediumMixin.css_class


class MediumPasswordField(MediumMixin, twbf.PasswordField):
    pass


class ProfileForm(twbf.HorizontalForm):

    user_name = MediumLabelField()
    display_name = MediumTextField()
#    last_name = twbf.TextField()
#    first_name = twbf.TextField()

    email_address = MediumTextField(validator=twc.EmailValidator)

    password_l = twbf.Label(text='Only if you want to change your password:', validator=twc.BlankValidator)
    password_1 = MediumPasswordField(label='New password')
    password_2 = MediumPasswordField(label='Repeat password')

    validator = FieldsMatch('password_1', 'password_2')

    def prepare(self):
        if getattr(self.value, 'disable_submit', False):  # pragma: no cover
            self.safe_modify('submit')
            self.submit.type = 'button'
            self.submit.value = 'Saving not possible'
            self.submit.css_class = 'btn btn-primary disabled'
        super(ProfileForm, self).prepare()


class RegistrationForm(twbf.HorizontalForm):

    user_name = MediumTextField()
    display_name = MediumTextField()
#    last_name = twbf.TextField()
#    first_name = twbf.TextField()

    email_address = MediumTextField(validator=twc.EmailValidator)

    password_1 = MediumPasswordField(label='New password')
    password_2 = MediumPasswordField(label='Repeat password')

    validator = FieldsMatch('password_1', 'password_2')
