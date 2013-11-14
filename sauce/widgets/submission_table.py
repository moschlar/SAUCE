# -*- coding: utf-8 -*-
'''Submission Listing Table for SAUCE

@see: :mod:`sprox`

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

import logging

from tg import request, flash, url

from sauce.model.user import lesson_members, team_members
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller

from sauce.model import Lesson, Submission, Team, User
import sauce.lib.helpers as h

from sauce.widgets.datagrid import JSSortableDataGrid
from webhelpers.html import literal

log = logging.getLogger(__name__)


def _actions(filler, subm):
    result = [u'<a href="%s/show" class="btn btn-mini" title="Show">'
        '<i class="icon-eye-open"></i></a>' % (subm.url)]
    delete_modal = u''
    if (subm.assignment.is_active
            and getattr(request, 'user', None) == subm.user):
        result.append(u'<a href="%s/edit" class="btn btn-mini" title="Edit">'
            '<i class="icon-pencil"></i></a>' % (subm.url))
    if (getattr(request, 'user', None) in subm.assignment.sheet.event.tutors
            or 'manage' in request.permissions):
        result.append(u'<a href="%s/judge" class="btn btn-mini" title="Judge">'
            '<i class="icon-tag"></i></a>' % (subm.url))
    if (getattr(request, 'user', None) in subm.assignment.sheet.event.tutors
            or getattr(request, 'user', None) == subm.user
            or 'manage' in request.permissions):
        result.append(u'<a class="btn btn-mini btn-danger" data-toggle="modal" '
            u'href="#deleteModal%d" title="Delete">'
            u'<i class="icon-remove icon-white"></i></a>' % (subm.id))
        delete_modal = u'''
<div class="modal hide fade" id="deleteModal%d">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal">×</button>
    <h3>Are you sure?</h3>
  </div>
  <div class="modal-body">
    <p>
      This will delete %s from the database.<br />
      You can not revert this step!
    </p>
  </div>
  <div class="modal-footer">
    <a href="#" class="btn" data-dismiss="modal">Cancel</a>
    <a href="%s/delete" class="btn btn-danger">
      <i class="icon-remove icon-white"></i>&nbsp;Delete&nbsp;%s
    </a>
  </div>
</div>
''' % (subm.id, unicode(subm), subm.url, unicode(subm))

    return literal('<div class="btn-group" style="width: %dpx;">'
        % (len(result) * 30) + ''.join(result) + '</div>' + delete_modal)


class SubmissionTable(TableBase):
    __model__ = Submission
    __omit_fields__ = ['source', 'assignment_id', 'language_id', 'user_id',
        'testruns', 'filename', 'complete']
    __field_order__ = ['id', 'user', 'team', 'assignment', 'language',
        'created', 'modified', 'result', 'judgement', 'grade', 'public']
    __add_fields__ = {'team': None, 'result': None, 'grade': None}
    __xml_fields__ = ['assignment', 'user', 'result', 'judgement', 'grade', 'public']
    __headers__ = {'public': u''}
    __base_widget_type__ = JSSortableDataGrid
    __base_widget_args__ = {'sortList': [[4, 0], [3, 0], [8, 1]],
        'headers': {0: {'sorter': False}, 6: {'sorter': False}}}


class SubmissionTableFiller(TableFiller):
    __model__ = Submission
    __omit_fields__ = ['source', 'assignment_id', 'language_id', 'user_id',
                       'testruns', 'filename', 'complete']
    __add_fields__ = {'team': None, 'result': None, 'grade': None}
    __actions__ = _actions

    def assignment(self, obj):
        try:
            a = obj.assignment
            l = h.link(obj.assignment.name, obj.assignment.url)
            if not a.is_active:
                l = literal('<i title="Assignment not active">') + l + literal('</i>')
            return l
        except AttributeError:
            log.warn('Submission %d has no assignment', obj.id)
            return u'<span class="label label-inverse">None</a>'

    def user(self, obj):
        try:
            if obj.user == request.user:
                return u'<em>%s</em>' % obj.user.display_name
            else:
                return obj.user.display_name
        except AttributeError:
            log.warn('Submission %d has no user', obj.id)
            return u'<span class="label label-inverse">None</a>'

    def team(self, obj):
        try:
            return u', '.join(t.name for t in set(obj.user.teams) & set(obj.assignment.sheet.event.teams))
        except:
            return u''

    def result(self, obj):
        if obj.result is not None:
            if obj.result:
                return u'<span class="label label-success">Success</a>'
            else:
                return u'<span class="label label-important">Failed</a>'
        else:
            return u'<span class="label">None</a>'

    def judgement(self, obj):
        if obj.judgement:
            return u'<a href="%s/judge" class="label label-info" title="%s">Yes</a>' % (obj.url, h.strftime(obj.judgement.date, False))
        else:
            return u'<a href="%s/judge" class="label">No</a>' % (obj.url)

    def grade(self, obj):
        if obj.judgement and obj.judgement.grade is not None:
            return u'<span class="badge badge-info">%s</span>' % unicode(obj.judgement.grade)
        else:
            return u''

    def public(self, obj):
        if obj.public:
            return u'<i class="icon-eye-open" title="Public">&nbsp;</i>'
        else:
            return u'<i class="icon-eye-close" title="Private">&nbsp;</i>'

    def created(self, obj):
        return h.strftime(obj.created, False)

    def modified(self, obj):
        return h.strftime(obj.modified, False)

    def __init__(self, *args, **kw):
        self.lesson = kw.pop('lesson', None)
        super(SubmissionTableFiller, self).__init__(*args, **kw)

    def _do_get_provider_count_and_objs(self, **kw):
        '''Custom getter function respecting lesson

        Returns the result count from the database and a query object
        '''

        qry = Submission.query

        # Process lesson filter
        if self.lesson:
            q1 = qry.join(Submission.user).join(lesson_members).join(Lesson).filter(Lesson.id == self.lesson.id).order_by(None)
            q2 = qry.join(Submission.user).join(team_members).join(Team).filter(Team.lesson_id == self.lesson.id).order_by(None)
            qry = q1.union(q2).distinct().order_by(Submission.id)

        filters = kw.pop('filters', dict())
        for filter in filters:
            if isinstance(filters[filter], (list, tuple, set)):
                qry = qry.filter(getattr(Submission, filter).in_(filters[filter]))
            else:
                qry = qry.filter(getattr(Submission, filter) == filters[filter])

        # Process filters from url
        kwfilters = kw
        exc = False
        try:
            kwfilters = self.__provider__._modify_params_for_dates(self.__model__, kwfilters)
        except ValueError as e:
            log.info('Could not parse date filters', exc_info=True)
            flash('Could not parse date filters: %s.' % e.message, 'error')
            exc = True

        try:
            kwfilters = self.__provider__._modify_params_for_relationships(self.__model__, kwfilters)
        except (ValueError, AttributeError) as e:
            log.info('Could not parse relationship filters', exc_info=True)
            flash('Could not parse relationship filters: %s. '
                  'You can only filter by the IDs of relationships, not by their names.' % e.message, 'error')
            exc = True
        if exc:
            # Since non-parsed kwfilters are bad, we just have to ignore them now
            kwfilters = {}

        for field_name, value in kwfilters.iteritems():
            field = getattr(self.__model__, field_name)
            try:
                if self.__provider__.is_relation(self.__model__, field_name) and isinstance(value, list):  # pragma: no cover
                    value = value[0]
                    qry = qry.filter(field.contains(value))
                else:
                    qry = qry.filter(field == value)
            except:
                log.warn('Could not create filter on query', exc_info=True)

        # Get total count
        count = qry.count()

        return count, qry
