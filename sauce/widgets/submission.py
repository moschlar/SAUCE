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
import tw2.jquery as twj

try:
    from tw2.jqplugins.chosen import ChosenSingleSelectField as _SingleSelectField
except ImportError:  # pragma: no cover
    from tw2.forms.bootstrap import SingleSelectField as _SingleSelectField

from sauce.widgets.lib import ays_js, make_cm_line_number_update_func, make_ays_init, make_cm_changes_save, make_cm_readonly_lines_func
from sauce.widgets.widgets import MyHorizontalLayout, MediumTextField, MediumMixin, LargeSourceEditor, SourceDisplay, SimpleWysihtml5
from sauce.model import Language, Assignment

log = logging.getLogger(__name__)


class SubmissionValidator(twc.Validator):

    def _validate_python(self, data, state=None):
        '''

        :type data: dict
        :type: sauce.model.Assignment
        :type: sauce.model.Submission
        '''
        controller = request.controller_state.controller
        assignment = controller.assignment
        submission = controller.submission

        language = data['language']
        if language not in assignment.allowed_languages:
            raise twc.ValidationError('The language %s is not allowed for this assignment' % (language))

        full_source, filename = u'', u''
        try:
            full_source = data['full_source']
            filename = (data['filename'] or
                'submission_%d.%s' % (submission.id, language.extension_src))
        except KeyError:  # pragma: no cover
            pass

        # TODO
        try:
            full_source = data['source_file'].value
            try:
                full_source = unicode(full_source, encoding='utf-8')
            except UnicodeDecodeError as e:
                log.info('UnicodeDecodeError in Submission %r: %s',
                    submission, e)
                try:
                    det = detect(full_source)
                    log.debug('Encoding detection for Submission %r returned %r', submission, det)
                    full_source = unicode(full_source, encoding=det['encoding'])
                    if det['confidence'] < 0.66:
                        flash('Your submission source code was automatically determined to be '
                              'of encoding %s. Please check for wrongly converted characters!' % det['encoding'],
                              'info')
                except (UnicodeDecodeError, TypeError) as e:  # TypeError occurs when det['encoding'] is None
                    if isinstance(e, UnicodeDecodeError):
                        log.info('UnicodeDecodeError in submission %r with detected encoding %s: %s',
                            submission, det['encoding'], e)
                    elif isinstance(e, TypeError):  # pragma: no cover
                        log.info('Could not determine encoding of Submission %r',
                            submission)
                    full_source = unicode(full_source, errors='ignore')
                    flash('Your submission source code failed to convert to proper Unicode. '
                          'Please verify your source code for replaced or missing characters. '
                          '(You should not be using umlauts in source code anyway...) '
                          'And even more should you not be submitting anything else but '
                          'source code text files here!',
                          'warning')
            filename = data['source_file'].filename
        except (KeyError, AttributeError):
            pass

        del data['source_file']
        data['filename'] = filename
        data['full_source'] = full_source

        try:
            source = assignment.strip_scaffold(full_source)
        except:
            log.debug('full_source=%r', full_source)
            log.info('Submission %r: scaffold modified', submission, exc_info=True)
            flash('Submission scaffold modified', 'error')
            raise twc.ValidationError('Submission scaffold modified')
        else:
            log.debug('source=%r', source)
            data['source'] = source

        return data

    # def from_python(self, value, state=None):
    #     print 'from_python', self, value, state  # TODO: print-Debugging
    #     return super(SubmissionValidator, self).from_python(value, state)


class LanguageSelectField(MediumMixin, _SingleSelectField):
    options = []
    prompt_text = None
    required = True
    validator = twsa.RelatedValidator(entity=Language)


class SubmissionForm(twbf.HorizontalForm):
    '''
    :type value: sauce.model.submission.Submission
    '''

    title = 'Submission'

    child = MyHorizontalLayout

    validator = SubmissionValidator

    id = twbf.HiddenField(validator=twc.IntValidator)
    assignment = twbf.HiddenField(validator=twsa.RelatedValidator(Assignment))

    filename = MediumTextField(
        placeholder=u'Enter a filename, if needed',
        validator=twc.StringLengthValidator,
        help_text=u'An automatically generated filename may not meet the '
        'language\'s requirements (e.g. the Java class name)',
    )

    full_source = LargeSourceEditor(
        label=u'Source',
        placeholder=u'Paste your source code here',
        validator=twc.StringLengthValidator(strip=False),
        fullscreen=True,
        foldGutter=True,
    )

    source_file = twbf.FileField(css_class='span7')

    language = LanguageSelectField()

    comment = SimpleWysihtml5(
        placeholder=u'Comment on the above source code',
        validator=twc.StringLengthValidator,
        rows=3,
    )

    @classmethod
    def post_define(cls):
        if twj.jquery_js not in cls.resources:
            cls.resources.append(twj.jquery_js)
        if ays_js not in cls.resources:
            cls.resources.append(ays_js)

    def prepare(self):
        self.safe_modify('language')
        self.child.c.language.options = [(l.id, l.name) for l in self.value.assignment.allowed_languages]
        if len(self.value.assignment.allowed_languages) == 1:
            self.value.language = self.value.assignment.allowed_languages[0]

        try:
            self.safe_modify('full_source')
            self.child.c.full_source.mode = self.value.language.lexer_name
            if self.value.scaffold_head or self.value.scaffold_foot:
                self.child.c.full_source.help_text = u'''\
The lines with grey background are the "scaffold" around your program, which you can't change.
'''
        except AttributeError:  # pragma: no cover
            pass

        super(SubmissionForm, self).prepare()

        self.add_call(make_ays_init(form=self.selector or 'Form'))

        self.add_call(make_cm_changes_save(selector=self.child.c.full_source.selector))

        self.add_call(make_cm_readonly_lines_func(value=self.value,
            selector=self.child.c.full_source.selector))
