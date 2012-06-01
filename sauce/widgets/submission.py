# -*- coding: utf-8 -*-
'''
Created on 17.03.2012

@author: moschlar
'''

import tw2.core as twc
import tw2.forms as twf
import tw2.bootstrap as twb
try:
    from tw2.jqplugins.chosen import ChosenSingleSelectField as SingleSelectField
except ImportError:
    from tw2.bootstrap import SingleSelectField


class SubmissionForm(twb.HorizontalForm):

    title = 'Submission'

    assignment_id = twf.HiddenField()
    submission_id = twf.HiddenField()

    filename = twb.TextField()
    source = twb.TextArea(cols=80, rows=8)
    source_file = twb.FileField()

    language_id = SingleSelectField(options=[], prompt_text=None,
        required=True, validator=twc.Required)

    def prepare(self):
        self.child.c.language_id.options = [(l.id, l.name) for l in self.value.assignment.allowed_languages]
        super(SubmissionForm, self).prepare()

    buttons = [
        twb.SubmitButton('test', name='test', value='Test', css_class='btn btn-primary'),
        twb.SubmitButton('submit', name='submit', value='Finish', css_class='btn btn-success'),
        twb.SubmitButton('reset', name='reset', value='Delete', css_class='btn btn-danger')]