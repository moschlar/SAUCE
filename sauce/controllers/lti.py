# -*- coding: utf-8 -*-
"""LTI controller module

Serves as a LTI tool provider

TODO: Tests
"""
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
from datetime import datetime

# turbogears imports
from tg import expose, url, redirect, flash, abort, request, session, tmpl_context as c
#from tg import redirect, validate, flash
from tg.decorators import with_trailing_slash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates
import status
from sqlalchemy import union
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import oauth2

# TODO: Nope!
from BeautifulSoup import BeautifulSoup

# project specific imports
from sauce.lib.base import BaseController
from sauce.model import DBSession, User, Assignment, Sheet, Event, Submission
from sauce.widgets.submission import SubmissionForm


log = logging.getLogger(__name__)


class LTIAssignmentController(BaseController):  # pragma: no cover
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()

    replace_result_request = '''
<?xml version = "1.0" encoding = "UTF-8"?>
<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">
  <imsx_POXHeader>
    <imsx_POXRequestHeaderInfo>
      <imsx_version>V1.0</imsx_version>
      <imsx_messageIdentifier>999999123</imsx_messageIdentifier>
    </imsx_POXRequestHeaderInfo>
  </imsx_POXHeader>
  <imsx_POXBody>
    <replaceResultRequest>
      <resultRecord>
        <sourcedGUID>
          <sourcedId>%(lis_result_sourcedid)s</sourcedId>
        </sourcedGUID>
        <result>
          <resultScore>
            <language>en</language>
            <textString>%(score)f</textString>
          </resultScore>
          <resultData>
            <text>%(data)s</text>
          </resultData>
        </result>
      </resultRecord>
    </replaceResultRequest>
  </imsx_POXBody>
</imsx_POXEnvelopeRequest>
'''

    def __init__(self, assignment, *args, **kwargs):
        self.assignment = assignment
        lti = assignment.lti or assignment.event.lti
        self.key = lti.oauth_key
        self.secret = lti.oauth_secret
        self.user = None
        self.submission = None
        super(LTIAssignmentController, self).__init__(*args, **kwargs)

    @expose()
    @with_trailing_slash
    def index(self, *args, **kwargs):
        try:
            server = oauth2.Server()
            server.add_signature_method(oauth2.SignatureMethod_HMAC_SHA1())
            req = oauth2.Request.from_request(request.method, request.url,
                request.headers, request.params, request.query_string)
            params = server.verify_request(req, oauth2.Consumer(self.key, self.secret), None)
        except:
            log.debug('LTI Tool Provider OAuth Error', exc_info=True)
            flash('LTI Tool Provider OAuth Error', 'error')
            abort(status.HTTP_403_FORBIDDEN)
        else:
            log.debug(params)

        user_name = (
            params.get('tool_consumer_info_product_family_code', 'external') + '_' +
            params.get('tool_consumer_instance_guid', 'external') + '_' +
            params.get('user_id'))

        user = User.query.filter_by(user_name=user_name).first()
        if not user:
            log.info('New user %s', user_name)
            user = User(
                user_name=user_name,
                display_name=params.get('lis_person_name_full'),
                email_address=params.get('lis_person_contact_email_primary'),
            )
            DBSession.add(user)

        submission = Submission.query.filter(Submission.assignment == self.assignment, Submission.user == user).first()
        if not submission:
            submission = Submission(
                assignment=self.assignment,
                filename=self.assignment.submission_filename or None,
                source=self.assignment.submission_template or None,
                language=self.assignment.allowed_languages[0],
                user=user,
                created=datetime.now(),
                modified=datetime.now(),
            )
            DBSession.add(submission)

            DBSession.flush()

        session['lti'] = True
        session['params'] = params
        session['user'] = user.id
        session['submission'] = submission.id
        session.save()

        redirect('/lti/%d/edit' % self.assignment.id)

    def _get_session_data(self):
        assert session['lti'] is True
        self.user = User.query.get(session['user'])
        self.submission = Submission.query.get(session['submission'])
#         self.heading = 'Submission for %s' % (
#             session['params'].get('resource_link_title', '') or
#             session['params'].get('context_title', '') or
#             'External Learning Tool')

    def _send_result(self, score, data):
        params = session['params']
        d = {'lis_result_sourcedid': params['lis_result_sourcedid'],
            'score': score, 'data': data}
        payload = self.replace_result_request % d

        client = oauth2.Client(oauth2.Consumer(self.key, self.secret))
        client.disable_ssl_certificate_validation = True
        h, r = client.request(
            uri=params['lis_outcome_service_url'], method='POST',
            body=payload.strip(), headers={'Content-Type': 'application/xml'})
        log.debug(h)
        # TODO: Nope!
        soup = BeautifulSoup(r)
        log.debug(soup)
        status = soup.find('imsx_codemajor').text == 'success'
        description = soup.find('imsx_description').text
        log.debug(status)
        log.debug(description)
        return status, description

    @expose('sauce.templates.ltiform')
    def edit(self, *args, **kwargs):
        self._get_session_data()
        c.form = SubmissionForm(action=url('./edit_'), value=self.submission)
        return dict(assignment=self.assignment, submission=self.submission, user=self.user)

    @expose('sauce.templates.ltiresult')
    def edit_(self, *args, **kwargs):
        self._get_session_data()

        v = SubmissionForm.validate(kwargs)
        language = v['language']
        source = v['source']
        filename = v['filename']

        self.submission.assignment = self.assignment
        self.submission.user = self.user
        if self.submission.language != language:
            self.submission.language = language
        if self.submission.source != source:
            self.submission.source = source
        if self.submission.filename != filename:
            self.submission.filename = filename
        if self.submission in DBSession.dirty:
            self.submission.modified = datetime.now()
            DBSession.add(self.submission)
        try:
            DBSession.flush()
        except SQLAlchemyError:
            DBSession.rollback()
            log.warn('Submission %r could not be saved', self.submission, exc_info=True)
            flash('Your submission could not be saved!', 'error')
            redirect('./edit')
        else:
#             redirect(self.submission.url + '/result')
            pass

        (compilation, testruns, result) = self.submission.run_tests()

        testruns = sorted(set(self.submission.testruns), key=lambda s: s.date)
        result = self.submission.result

        if result is True:
            score = 1.0
        else:
            if testruns:
                score = (float(len([t for t in testruns if t.result])) / float(len(testruns)))
            else:
                score = 0.0
        send = self._send_result(score, str(result))
        log.info(send)

        return dict(assignment=self.assignment, submission=self.submission, user=self.user,
            compilation=compilation, testruns=testruns, result=result, score=score)


class LTIController(BaseController):  # pragma: no cover
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()

    @expose()
    def index(self, *args, **kwargs):
        flash('LTI Tool Provider', 'warn')
        abort(status.HTTP_400_BAD_REQUEST)

    @expose()
    @with_trailing_slash
    def _lookup(self, assignment_id, *args):
        try:
            assignment_id = int(assignment_id)
            # TODO: Use SQLAlchemy magic on model to make queries on assignment easier
            q1 = (Assignment.query.filter(Assignment.id == assignment_id)
                .join(Assignment._lti).order_by(None))
            q2 = (Assignment.query.filter(Assignment.id == assignment_id)
                .join(Sheet).join(Event).join(Event.lti).order_by(None))
            assignment = Assignment.query.select_entity_from(union(q1, q2)).one()
        except ValueError:
            flash('Invalid LTI Assignment id: %s' % assignment_id, 'error')
            abort(status.HTTP_400_BAD_REQUEST)
        except NoResultFound:
            flash('LTI Assignment %d not found' % assignment_id, 'error')
            abort(status.HTTP_404_NOT_FOUND)
        except MultipleResultsFound:  # pragma: no cover
            log.error('Database inconsistency: LTI Assignment %d', assignment_id, exc_info=True)
            flash('An error occurred while accessing LTI Assignment %d' % assignment_id, 'error')
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

        controller = LTIAssignmentController(assignment)
        return controller, args
