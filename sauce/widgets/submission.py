# -*- coding: utf-8 -*-
'''
Created on 17.03.2012

@author: moschlar
'''

import tw2.core as twc
import tw2.forms as twf
import tw2.bootstrap as twb
import tw2.jqplugins.chosen as tw_j_c

from sauce.model import Language, Assignment


class SubmissionForm(twb.HorizontalForm):

    assignment_id = twf.HiddenField()
    submission_id = twf.HiddenField()

    filename = twb.TextField()
    source = twb.TextArea()
    source_file = twb.FileField()

    #language_id = twb.SingleSelectField(options=[], required=True)
    language_id = tw_j_c.ChosenSingleSelectField(options=[], required=True)

    def prepare(self):
        self.child.c.language_id.options = self.value.assignment.allowed_languages
        super(SubmissionForm, self).prepare()
