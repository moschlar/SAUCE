# -*- coding: utf-8 -*-
'''
Created on 17.03.2012

@author: moschlar
'''
import tw2.core as twc
import tw2.bootstrap.forms as twbf

try:
    from tw2.ace import AceWidget as SourceEditor
#    from tw2.codemirror import CodeMirrorWidget as SourceEditor
except ImportError:
    from tw2.bootstrap.forms import TextArea as SourceEditor

try:
    from tw2.jqplugins.chosen import ChosenSingleSelectField as SingleSelectField
except ImportError:
    from tw2.forms.bootstrap import SingleSelectField


class SubmissionForm(twbf.HorizontalForm):

    title = 'Submission'

    id = twbf.HiddenField(validator=twc.IntValidator)
    assignment_id = twbf.HiddenField(validator=twc.IntValidator)

    filename = twbf.TextField(placeholder=u'Enter a filename, if needed',
        help_text=u'An automatically generated filename may not meet the '\
        'language\'s requirements (e.g. the Java class name)',
        css_class='span3')
    source = SourceEditor(placeholder=u'Paste your source code here',
        css_class='span8', cols=80, rows=10)
    source_file = twbf.FileField(css_class='span7')

    language_id = SingleSelectField(options=[], prompt_text=None,
        css_class='span3',
        required=True, validator=twc.IntValidator(required=True))

    def prepare(self):
        self.safe_modify('language_id')
        self.child.c.language_id.options = [(l.id, l.name) for l in self.value.assignment.allowed_languages]
        try:
            self.safe_modify('source')
            self.child.c.source.mode = self.value.language.lexer_name
        except AttributeError:
            pass
        super(SubmissionForm, self).prepare()
