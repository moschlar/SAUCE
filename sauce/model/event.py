# -*- coding: utf-8 -*-
'''Event model module

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

from sqlalchemy import Column, ForeignKey, Index, UniqueConstraint
from sqlalchemy.types import Integer, Unicode, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase
from sauce.lib.helpers import link
from sauce.model.user import lesson_members, User
from warnings import warn


class Event(DeclarativeBase):
    '''An Event'''
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    type = Column(Enum('course', 'contest', name='event_type'), nullable=False)
    
    _url = Column('url', String(255), nullable=False, index=True, unique=True)
    
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(65536))
    
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime, nullable=False, default=lambda: datetime.now() + timedelta(days=31))
    
    password = Column(Unicode(255))
    '''The password students have to enter in order to enroll to an event'''
    
    public = Column(Boolean, nullable=False, default=True)
    '''Whether this Event is shown to non-logged in users and non-enrolled students'''
    
    teacher_id = Column(Integer, ForeignKey('users.id'))
    teacher = relationship('User',
        #backref=backref('events',
        #    cascade='all, delete-orphan')
        )
    '''The main teacher, displayed as contact on event details'''
    
    __mapper_args__ = {'polymorphic_on': 'type',
                       'order_by': [end_time, start_time, _url]}
    
    def __unicode__(self):
        return self.name
    
    #----------------------------------------------------------------------------
    # Properties
    
    @property
    def current_sheets(self):
        return [s for s in self.sheets if s.start_time < datetime.now() and s.end_time > datetime.now()]
    
    @property
    def previous_sheets(self):
        return [s for s in self.sheets if s.end_time < datetime.now()]
    
    @property
    def future_sheets(self):
        return [s for s in self.sheets if s.start_time > datetime.now()]
    
    @property
    def public_sheets(self):
        return [s for s in self.sheets if s.public]
    
    @property
    def url(self):
        return '/events/%s' % self._url
    
    @property
    def link(self):
        '''Link for this event'''
        return link(self.name, self.url)
    
    @property
    def breadcrumbs(self):
        '''Array of links for breadcrumb navigation'''
        return [self.link]
    
    parent = None

    @property
    def teams(self):
        t = set()
        for l in self.lessons:
            t |= set(l.teams)
        return t

    @property
    def children(self):
        return self.sheets
    
    @property
    def is_active(self):
        '''If the event is active at the moment'''
        return self.start_time < datetime.now() < self.end_time
    
    @property
    def remaining_time(self):
        '''Remaining time for event'''
        return max(self.end_time - datetime.now(), timedelta(0))
    
    @property
    def tutors(self):
        return [l.tutor for l in self.lessons]

    @property
    def teachers(self):
        warn('The teachers attribute is deprecated')
        return self.tutors

    @property
    def members(self):
        studs = set()
        for l in self.lessons:
            studs |= set(l.members)
        return studs

    @property
    def students(self):
        warn('The students attribute is deprecated')
        return self.members

    #----------------------------------------------------------------------------
    # Classmethods
    
    @classmethod
    def by_url(cls, url):
        '''Return the event specified by url'''
        return cls.query.filter(cls._url == url).one()
    
#    @classmethod
#    def all_events(cls, only_public=True):
#        '''Return a 3-tuple (current, previous, future) containing all events'''
#        return (cls.current_events(only_public).all(), 
#                cls.previous_events(only_public).all(), 
#                cls.future_events(only_public).all())

    @classmethod
    def current_events(cls, only_public=False):
        '''Return a query for currently active events'''
        q = cls.query
        if only_public:
            q = q.filter_by(public=True)
        q = q.filter(cls.start_time < datetime.now()).filter(cls.end_time > datetime.now())
        return q

    @classmethod
    def previous_events(cls, only_public=False):
        '''Return a query for previously active events'''
        q = cls.query
        if only_public:
            q = q.filter_by(public=True)
        q = q.filter(cls.end_time < datetime.now())
        return q

    @classmethod
    def future_events(cls, only_public=False):
        '''Return a query for future active events'''
        q = cls.query
        if only_public:
            q = q.filter_by(public=True)
        q = q.filter(cls.start_time > datetime.now())
        return q


class Course(Event):
    '''An Event with type course'''
    __mapper_args__ = {'polymorphic_identity': 'course'}


class Contest(Event):
    '''An Event with type contest'''
    __mapper_args__ = {'polymorphic_identity': 'contest'}


class Lesson(DeclarativeBase):
    '''A Lesson'''
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)

    lesson_id = Column(Integer, index=True, nullable=False)
    '''The lesson_id specific to the parent event'''

    _url = Column('url', String(255))
    '''Not used right now!'''

    name = Column(Unicode(255), nullable=False)

    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship('Event',
        backref=backref('lessons',
            order_by=lesson_id,
            cascade='all, delete-orphan')
        )

    tutor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tutor = relationship('User',
        backref=backref('tutored_lessons',
            order_by=lesson_id,
            cascade='all, delete-orphan')
        )

    _members = relationship('User',
        secondary=lesson_members,
        order_by='User.user_name',
        backref=backref('_lessons',
            order_by=lesson_id)
        )

    __table_args__ = (
        UniqueConstraint('event_id', 'lesson_id'),
        Index('idx_event_lesson', event_id, lesson_id, unique=True)
        )

    def __unicode__(self):
        return u'Lesson "%s"' % (self.name)

    @property
    def url(self):
        return self.event.url + '/lessons/%s' % self.lesson_id

    @property
    def link(self):
        '''Link for this lesson'''
        return link(self.name, self.url)

    @property
    def breadcrumbs(self):
        '''Array of links for breadcrumb navigation'''
        return self.event.breadcrumbs + [self.link]

    @property
    def members(self):
        s = set(self._members)
        for t in self.teams:
            s |= set(t.members)
        return s

    @property
    def students(self):
        warn('The students attribute is deprecated')
        return self.members

    @property
    def teacher(self):
        warn('The teacher attribute is deprecated')
        return self.tutor

    #----------------------------------------------------------------------------
    # Classmethods

    @classmethod
    def by_lesson_id(cls, lesson_id, event):
        return cls.query.filter(cls.event_id == event.id).filter(cls.lesson_id == lesson_id).one()
