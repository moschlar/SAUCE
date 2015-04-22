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

from sqlalchemy import Column, ForeignKey, Table, or_, and_, Index, UniqueConstraint
from sqlalchemy.types import Integer, Unicode, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.sql.expression import desc

from sauce.model import DeclarativeBase, metadata, DBSession, curr_prev_future
from sauce.lib.helpers import link
from sauce.model.submission import Submission


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
#        Index('idx_event_assignment', event_id, assignment_id, unique=True),
    )

    def __repr__(self):
        return (u'<Assignment: id=%r, sheet_id=%r, assignment_id=%r, name=%r>'
            % (self.id, self.sheet_id, self.assignment_id, self.name)
        ).encode('utf-8')

    def __unicode__(self):
        return u'Assignment "%s"' % self.name

    def clone(self, i=0, recursive=True):
        a = Assignment(**dict((k, v) for (k, v) in vars(self).items()
            if k != 'id' and k != '_sa_instance_state'))
        a.assignment_id = Assignment.query\
            .filter(Assignment.sheet_id == self.sheet_id)\
            .filter(Assignment.assignment_id >= self.assignment_id)\
            .order_by(desc(Assignment.assignment_id)).first().assignment_id + i + 1
        a.allowed_languages = [l for l in self.allowed_languages]
        if recursive:
            a.tests = [t.clone() for t in self.tests]
        return a

    #----------------------------------------------------------------------------
    # Properties

    @property
    def url(self):
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
        '''Parent entity for generic hierarchy traversal'''
        return self.sheet

    @property
    def event(self):
#         return self._event or self.sheet.event
        return self.sheet.event

    @property
    def teacher(self):
        return self._teacher or self.sheet.teacher

    @property
    def visible_tests(self):  # pragma: no cover
        warn('Assignment.visible_tests', DeprecationWarning, stacklevel=2)
        return [test for test in self.tests if test.visibility == 'visible']

    @property
    def invisible_tests(self):  # pragma: no cover
        warn('Assignment.invisible_tests', DeprecationWarning, stacklevel=2)
        return [test for test in self.tests if test.visibility == 'invisible']

    @property
    def start_time(self):
        if self._start_time:
            return self._start_time
        elif self.sheet:
            return self.sheet.start_time
        elif self.event:
            return self.event.start_time
        raise Exception('No start_time')

    @property
    def end_time(self):
        if self._end_time:
            return self._end_time
        elif self.sheet:
            return self.sheet.end_time
        elif self.event:
            return self.event.end_time
        raise Exception('No end_time')

    @property
    def is_active(self):
        return self.start_time < datetime.now() < self.end_time

    @property
    def remaining_time(self):
        return max(self.end_time - datetime.now(), timedelta(0))

    @property
    def lti(self):
        return self._lti or self.event.lti

    @property
    def lti_url(self):
        return '/lti/%d/' % self.id

    def submissions_by_user(self, user, team=False):
        ids = [user.id]
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
        s = Sheet(**dict((k, v) for (k, v) in vars(self).items()
            if k != 'id' and k != '_sa_instance_state'))
        s.sheet_id = Sheet.query\
            .filter(Sheet.event_id == self.event_id)\
            .filter(Sheet.sheet_id >= self.sheet_id)\
            .order_by(desc(Sheet.sheet_id)).first().sheet_id + i + 1
        if recursive:
            s.assignments = [a.clone(i=i, recursive=recursive) for i, a in enumerate(self.assignments)]
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
#
#    @classmethod
#    def by_url(cls, url):
#        return cls.query.filter(cls.url == url).one()
#
#    @classmethod
#    def all_sheets(cls, event=None, only_public=True):
#        '''Return a 3-tuple (current, previous, future) containing all sheets'''
#        return curr_prev_future(cls.current_sheets(event, only_public),
#                cls.previous_sheets(event, only_public),
#                cls.future_sheets(event, only_public))
#
#    @classmethod
#    def current_sheets(cls, event=None, only_public=True):
#        '''Return currently active sheets'''
#        q = cls.query
#        if event:
#            q = q.filter_by(event_id=event.id)
#        if only_public:
#            q = q.filter_by(public=True)
#        return [s for s in q.all() if s.start_time < datetime.now() and s.end_time > datetime.now()]
#        q = q.filter(cls.start_time < datetime.now()).filter(cls.end_time > datetime.now())
#        q = q.filter(or_(
#                         and_(cls._start_time != None, cls._end_time != None,
#                              cls._start_time < datetime.now(), cls._end_time > datetime.now()),
#                         and_(datetime.now() > DBSession.query(Event.start_time).filter(Event.id==event.id).scalar(),
#                              datetime.now() < DBSession.query(Event.end_time).filter(Event.id==event.id).scalar())
#                         ))
#        return q.all()
#
#    @classmethod
#    def previous_sheets(cls, event=None, only_public=True):
#        '''Return a query for previously active sheets'''
#        q = cls.query
#        if event:
#            q = q.filter_by(id=event.id)
#        if only_public:
#            q = q.filter_by(public=True)
#        return [s for s in q.all() if datetime.now() > s.end_time]
#        #q = q.filter(cls.end_time < datetime.now())
#
#    @classmethod
#    def future_sheets(cls, event=None, only_public=True):
#        '''Return a query for future active sheets'''
#        q = cls.query
#        if event:
#            q = q.filter_by(id=event.id)
#        if only_public:
#            q = q.filter_by(public=True)
#        return [s for s in q.all() if s.start_time > datetime.now()]
#        #q = q.filter(cls.start_time > datetime.now())
