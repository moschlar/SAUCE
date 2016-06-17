# -*- coding: utf-8 -*-
'''Assignment model module

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

from datetime import datetime, timedelta
from warnings import warn

from tg.caching import cached_property

from sqlalchemy import Column, ForeignKey, Index, Table, UniqueConstraint
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import backref, deferred, relationship
from sqlalchemy.types import Boolean, DateTime, Float, Integer, String, Unicode

from sauce.lib.helpers import link
from sauce.model import DBSession, DeclarativeBase, metadata
from sauce.model.submission import Submission


__all__ = ('Assignment', 'Sheet')


class ScaffoldException(Exception): pass


# secondary table for many-to-many relation
language_to_assignment = Table('language_to_assignment', metadata,
    Column('language_id', Integer, ForeignKey('languages.id'), primary_key=True),
    Column('assignment_id', Integer, ForeignKey('assignments.id'), primary_key=True)
)


class Assignment(DeclarativeBase):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True, nullable=False)

    assignment_id = Column(Integer, nullable=False, index=True,
        doc='The assignment_id specific to the parent sheet')

#     _url = Column('url', String(255), nullable=True)
#     '''Not used right now!'''

    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(64 * 1024), nullable=True)

#     event_id = Column(Integer, ForeignKey('events.id'), nullable=True, index=True)
#     _event = relationship('Event',
#         backref=backref('_assignments',
#             order_by=assignment_id,
#             cascade='all, delete-orphan',
#         )
#     )

    _start_time = Column('start_time', DateTime, nullable=True)
    _end_time = Column('end_time', DateTime, nullable=True)

    timeout = Column(Float, nullable=True, default=10.0)

    allowed_languages = relationship('Language', secondary=language_to_assignment)

    show_compiler_msg = Column(Boolean, nullable=False, default=True)

    teacher_id = Column(Integer, ForeignKey('users.id'))
    _teacher = relationship('User',
        #backref=backref('assignments',
        #    cascade='all, delete-orphan')
        doc='The Teacher that created this assignment'
    )

    sheet_id = Column(Integer, ForeignKey('sheets.id'), nullable=True, index=True)
    sheet = relationship('Sheet',
        backref=backref('assignments',
            order_by=assignment_id,
            cascade='all, delete-orphan',
        )
    )

    public = Column(Boolean, nullable=False, default=True,
        doc='Whether this Assignment is shown to non-logged in users and non-enrolled students')

    submission_filename = deferred(Column(Unicode(255), nullable=True), group='data',
        doc='Submission default filename')
    submission_template = deferred(Column(Unicode(10485760), nullable=True), group='data',
        doc='Submission body template')
    submission_scaffold_show = Column(Boolean, nullable=False, default=False,
        doc='Whether to show head and foot scaffold to student')
    submission_scaffold_head = deferred(Column(Unicode(10485760), nullable=True), group='data',
        doc='Submission head part of scaffold')
    submission_scaffold_foot = deferred(Column(Unicode(10485760), nullable=True), group='data',
        doc='Submission foot part of scaffold')

    __mapper_args__ = {'order_by': [_end_time, _start_time, assignment_id]}
    __table_args__ = (
        UniqueConstraint(sheet_id, assignment_id),
        Index('idx_sheet_assignment', sheet_id, assignment_id, unique=True),
        # Index('idx_event_assignment', event_id, assignment_id, unique=True),
    )

    def __repr__(self):
        return (u'<Assignment: id=%r, sheet_id=%r, assignment_id=%r, name=%r>'
            % (self.id, self.sheet_id, self.assignment_id, self.name)
        ).encode('utf-8')

    def __unicode__(self):
        return u'Assignment "%s"' % self.name

    def clone(self, i=0, recursive=True):
        a = Assignment(**dict((attr.key, getattr(self, attr.key)) for attr in inspect(self).mapper.column_attrs
            if attr.key != 'id'))
        a.assignment_id = i + 1  # TODO: Not uniqueness-safe
        a.allowed_languages = [l for l in self.allowed_languages]
        if recursive:
            a.tests = [t.clone(i=j) for j, t in enumerate(self.tests)]
        return a

    #----------------------------------------------------------------------------
    # Properties

    @property
    def url(self):
        ''':rtype: str | None'''
        if self.sheet:
            return self.sheet.url + '/assignments/%s' % self.assignment_id
        else:
            return None

    @property
    def link(self):
        '''Link for this Assignment'''
        return link(self.name, self.url)

    @property
    def breadcrumbs(self):
        '''Array of links for breadcrumb navigation'''
        return self.sheet.breadcrumbs + [self.link]

    @property
    def parent(self):
        '''Parent entity for generic hierarchy traversal

        :rtype: sauce.model.Sheet
        '''
        return self.sheet

    @property
    def event(self):
        ''':rtype: sauce.model.Event'''
        # return self._event or self.sheet.event
        return self.sheet.event

    @property
    def teacher(self):
        ''':rtype: sauce.model.User'''
        return self._teacher or self.sheet.teacher

    @property
    def visible_tests(self):  # pragma: no cover
        ''':rtype: list[sauce.model.Test]'''
        warn('Assignment.visible_tests', DeprecationWarning, stacklevel=2)
        return [test for test in self.tests if test.visibility == 'visible']

    @property
    def invisible_tests(self):  # pragma: no cover
        ''':rtype: list[sauce.model.Test]'''
        warn('Assignment.invisible_tests', DeprecationWarning, stacklevel=2)
        return [test for test in self.tests if test.visibility == 'invisible']

    @property
    def start_time(self):
        ''':rtype: datetime'''
        if self._start_time:
            return self._start_time
        elif self.sheet:
            return self.sheet.start_time
        elif self.event:
            return self.event.start_time
        raise Exception('No start_time')

    @property
    def end_time(self):
        ''':rtype: datetime'''
        if self._end_time:
            return self._end_time
        elif self.sheet:
            return self.sheet.end_time
        elif self.event:
            return self.event.end_time
        raise Exception('No end_time')

    @property
    def is_active(self):
        ''':rtype: bool'''
        return self.start_time < datetime.now() < self.end_time

    @property
    def remaining_time(self):
        ''':rtype: timedelta'''
        return max(self.end_time - datetime.now(), timedelta(0))

    @property
    def lti(self):
        ''':rtype: sauce.model.LTI | None'''
        return self._lti or self.event.lti

    @property
    def lti_url(self):
        ''':rtype: str'''
        return '/lti/%d/' % self.id

    @cached_property
    def submission_scaffold_head_lines(self):
        ''':rtype: list[str] | None'''
        return self.submission_scaffold_head.splitlines() if self.submission_scaffold_head else None

    @cached_property
    def submission_scaffold_head_lines_len(self):
        ''':rtype: int'''
        return len(self.submission_scaffold_head_lines) if self.submission_scaffold_head_lines else 0

    @cached_property
    def submission_scaffold_foot_lines(self):
        ''':rtype: list[str] | None'''
        return self.submission_scaffold_foot.splitlines() if self.submission_scaffold_foot else None

    @cached_property
    def submission_scaffold_foot_lines_len(self):
        ''':rtype: int'''
        return len(self.submission_scaffold_foot_lines) if self.submission_scaffold_foot_lines else 0

    def strip_scaffold(self, full_source):
        '''Strip head and foot scaffold off full_source

        # FIXME: This essentially converts all newlines here, but this should really rather be handled once and for all

        :type full_source: str
        :rtype: str
        :raises ScaffoldException: if full_source is not exactly surrounded by scaffold_{head,foot}
        '''
        source_lines = full_source.splitlines()

        if self.submission_scaffold_head:
            for i, (a, b) in enumerate(zip(self.submission_scaffold_head_lines, source_lines)):
                if a != b:
                    raise ScaffoldException('scaffold_head', i, a, b)
            source_lines = source_lines[self.submission_scaffold_head_lines_len:]

        if self.submission_scaffold_foot:
            for i, (a, b) in enumerate(zip(reversed(self.submission_scaffold_foot_lines), reversed(source_lines))):
                if a != b:
                    raise ScaffoldException('scaffold_foot', i, a, b)
            source_lines = source_lines[:-self.submission_scaffold_foot_lines_len]

        return '\n'.join(source_lines)

    def submissions_by_user(self, user, team=False):
        ''':rtype: list[Submission]'''  # FIXME: Not really a list, but...
        ids = [user.id]  # TODO: set?
        if team:
            try:
                teams = set((t for l in self.sheet.event.lessons for t in l.teams)) & set(user.teams)
                for team in teams:
                    ids.extend((u.id for u in team.members))
            except:
                pass
        return (Submission.query.filter_by(assignment_id=self.id).filter(Submission.user_id.in_(ids))
            .order_by(Submission.user_id))

    #----------------------------------------------------------------------------
    # Classmethods

    @classmethod
    def by_assignment_id(cls, assignment_id, sheet):
        ''':rtype: sauce.model.Assignment'''
        return cls.query.filter(cls.sheet_id == sheet.id).filter(cls.assignment_id == assignment_id).one()


class Sheet(DeclarativeBase):
    '''A Sheet'''
    __tablename__ = 'sheets'

    id = Column(Integer, primary_key=True, nullable=False)

    sheet_id = Column(Integer, nullable=False, index=True,
        doc='The sheet_id specific to the parent event')

#     _url = Column('url', String(255))
#     '''Not used right now!'''

    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(64 * 1024), nullable=True)

    event_id = Column(Integer, ForeignKey('events.id'), nullable=False, index=True)
    event = relationship("Event",
        backref=backref('sheets',
            order_by=sheet_id,
            cascade='all, delete-orphan',
        )
    )

    _start_time = Column('start_time', DateTime, nullable=True)
    _end_time = Column('end_time', DateTime, nullable=True)

    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    _teacher = relationship('User',
        #backref=backref('sheets',
        #    cascade='all, delete-orphan')
        doc='The Teacher that created this sheet'
    )

    public = Column(Boolean, nullable=False, default=True,
        doc='Whether this Sheet is shown to non-logged in users and non-enrolled students')

    __mapper_args__ = {'order_by': [_end_time, _start_time, sheet_id]}
    __table_args__ = (Index('idx_event_sheet', event_id, sheet_id, unique=True),)

    def __repr__(self):
        return (u'<Sheet: id=%r, event_id=%r, sheet_id=%r, name=%r>'
            % (self.id, self.event_id, self.sheet_id, self.name)
        ).encode('utf-8')

    def __unicode__(self):
        return u'Sheet "%s"' % self.name

    def clone(self, i=0, recursive=True):
        s = Sheet(**dict((attr.key, getattr(self, attr.key)) for attr in inspect(self).mapper.column_attrs
            if attr.key != 'id'))
        s.sheet_id = i + 1  # TODO: Not uniqueness-safe
        if recursive:
            s.assignments = [a.clone(i=j, recursive=recursive) for j, a in enumerate(self.assignments)]
        return s

    #----------------------------------------------------------------------------
    # Properties

    @property
    def url(self):
        return self.event.url + '/sheets/%s' % self.sheet_id

    @property
    def link(self):
        '''Link for this Sheet'''
        return link(self.name, self.url)

    @property
    def breadcrumbs(self):
        '''Array of links for breadcrumb navigation'''
        return self.event.breadcrumbs + [self.link]

    @property
    def parent(self):
        '''Parent entity for generic hierarchy traversal'''
        return self.event

    @property
    def children(self):
        return self.assignments

    @property
    def teacher(self):
        return self._teacher or self.event.teacher  # TODO

    @property
    def start_time(self):
        return self._start_time or self.event.start_time

    @property
    def end_time(self):
        return self._end_time or self.event.end_time

    @property
    def is_active(self):
        '''If the Sheet is active at the moment'''
        return self.start_time < datetime.now() < self.end_time

    @property
    def remaining_time(self):
        '''Remaining time for Sheet'''
        return max(self.end_time - datetime.now(), timedelta(0))

    #----------------------------------------------------------------------------
    # Classmethods

    @classmethod
    def by_sheet_id(cls, sheet_id, event):
        return cls.query.filter(cls.event_id == event.id).filter(cls.sheet_id == sheet_id).one()

#    @classmethod
#    def by_url(cls, url):
#        return cls.query.filter(cls.url == url).one()
