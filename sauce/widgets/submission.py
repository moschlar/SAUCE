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

from sauce.model import Language, Assignment


class SubmissionForm(twb.HorizontalForm):

    assignment_id = twf.HiddenField()
    submission_id = twf.HiddenField()

    filename = twb.TextField()
    source = twb.TextArea(cols=80, rows=8)
    source_file = twb.FileField()

    language_id = SingleSelectField(options=[], required=True)

    def prepare(self):
        self.child.c.language_id.options = [(l.id, l.name) for l in self.value.assignment.allowed_languages]
        if len(self.value.assignment.allowed_languages) > 1:
            self.child.c.language_id.options.insert(0, ('', ''))
        super(SubmissionForm, self).prepare()
