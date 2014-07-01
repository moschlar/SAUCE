# -*- coding: utf-8 -*-
'''Submission widget for SAUCE

:class:`SubmissionValidator` handles the data which comes from either
the text fields or from an uploaded file.

@since: 17.03.2012
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

import logging

from chardet import detect

from tg import flash, request

import tw2.core as twc
import tw2.bootstrap.forms as twbf
import tw2.sqla as twsa

from tw2.pygmentize import Pygmentize as _Pygmentize

try:
    from tw2.ace import AceWidget as SourceEditor
#    from tw2.codemirror import CodeMirrorWidget as SourceEditor
except ImportError:  # pragma: no cover
    from tw2.bootstrap.forms import TextArea as SourceEditor

try:
    from tw2.jqplugins.chosen import ChosenSingleSelectField as _SingleSelectField
except ImportError:  # pragma: no cover
    from tw2.forms.bootstrap import SingleSelectField as _SingleSelectField

from sauce.widgets.widgets import MediumTextField, MediumMixin
from sauce.model import Language, Assignment

log = logging.getLogger(__name__)


class Pygmentize(_Pygmentize):
    value = twc.Param(default=None)
    show = twc.Param(default=True)

    def prepare(self):
        self.source = self.value
        if self.show and self.source:
            super(Pygmentize, self).prepare()
        else:
            self.label = None
            self.source = u''


class SubmissionValidator(twc.Validator):

    def _validate_python(self, data, state=None):
        controller = request.controller_state.controller
        submission = controller.submission

        language = data['language']
        if language not in controller.assignment.allowed_languages:
            raise twc.ValidationError('The language %s is not allowed for this assignment' % (language))

        source, filename = u'', u''
        try:
            source = data['source']
            filename = (data['filename'] or
                'submission_%d.%s' % (submission.id, language.extension_src))
        except KeyError:
            pass

        # TODO
        try:
            source = data['source_file'].value
            try:
                source = unicode(source, encoding='utf-8')
            except UnicodeDecodeError as e:
                log.info('UnicodeDecodeError in Submission %r: %s',
                    submission, e)
                try:
                    det = detect(source)
                    log.debug('Encoding detection for Submission %r returned %r', submission, det)
                    source = unicode(source, encoding=det['encoding'])
                    if det['confidence'] < 0.66:
                        flash('Your submission source code was automatically determined to be '
                              'of encoding %s. Please check for wrongly converted characters!' % det['encoding'],
                              'info')
                except (UnicodeDecodeError, TypeError) as e:  # TypeError occurs when det['encoding'] is None
                    if isinstance(e, UnicodeDecodeError):
                        log.info('UnicodeDecodeError in submission %r with detected encoding %s: %s',
                            submission, det['encoding'], e)
                    elif isinstance(e, TypeError):
                        log.info('Could not determine encoding of Submission %r',
                            submission)
                    source = unicode(source, errors='ignore')
                    flash('Your submission source code failed to convert to proper Unicode. '
                          'Please verify your source code for replaced or missing characters. '
                          '(You should not be using umlauts in source code anyway...) '
                          'And even more should you not be submitting anything else but '
                          'source code text files here!',
                          'warning')
            filename = data['source_file'].filename
        except (KeyError, AttributeError):
            pass

#         data['source_file'] = None
        del data['source_file']
        data['source'] = source
        data['filename'] = filename
        return data


class LanguageSelectField(MediumMixin, _SingleSelectField):
    options = []
    prompt_text = None
    required = True
    validator = twsa.RelatedValidator(entity=Language)


class SubmissionForm(twbf.HorizontalForm):

    title = 'Submission'

    validator = SubmissionValidator

    id = twbf.HiddenField(validator=twc.IntValidator)
    assignment = twbf.HiddenField(validator=twsa.RelatedValidator(Assignment))

    filename = MediumTextField(
        placeholder=u'Enter a filename, if needed',
        validator=twc.StringLengthValidator,
        help_text=u'An automatically generated filename may not meet the '
        'language\'s requirements (e.g. the Java class name)',
    )
    scaffold_head = Pygmentize()
    source = SourceEditor(
        placeholder=u'Paste your source code here',
        validator=twc.StringLengthValidator,
        css_class='span8', cols=80, rows=24)
    scaffold_foot = Pygmentize()
    source_file = twbf.FileField(css_class='span7')

    language = LanguageSelectField()

#TODO: Probably show scaffold here

    def prepare(self):
        self.safe_modify('language')
        self.child.c.language.options = [(l.id, l.name) for l in self.value.assignment.allowed_languages]
        try:
            self.safe_modify('source')
            self.child.c.source.mode = self.value.language.lexer_name
        except AttributeError:
            pass
        try:
            self.safe_modify('scaffold_head')
            self.child.c.scaffold_head.lexer_name = self.value.language.lexer_name
            self.child.c.scaffold_head.filename = self.value.filename
            self.child.c.scaffold_head.show = self.value.scaffold_show
        except AttributeError:
            pass
        try:
            self.safe_modify('scaffold_foot')
            self.child.c.scaffold_foot.lexer_name = self.value.language.lexer_name
            self.child.c.scaffold_foot.filename = self.value.filename
            self.child.c.scaffold_foot.show = self.value.scaffold_show
        except AttributeError:
            pass
        super(SubmissionForm, self).prepare()
