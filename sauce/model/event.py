# -*- coding: utf-8 -*-
'''Event model module

@author: moschlar
'''

from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase
from sauce.lib.helpers import link_

class Event(DeclarativeBase):
    '''An Event'''
    __tablename__ = 'events'
    __mapper_args__ = {'polymorphic_on': 'type', 'order_by': ['end_time', 'start_time']}
    
    id = Column(Integer, primary_key=True)
    type = Column(Enum('course', 'contest'), nullable=False)
    
    url = Column(String(255), index=True, unique=True)
    
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(65536))
    
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime, nullable=False, default=datetime.now)
    
    password = Column(Unicode(255))
    '''The password students have to enter in order to enroll to an event'''
    
    public = Column(Boolean, nullable=False, default=False)
    '''Whether this Event is shown to non-logged in users and non-enrolled students'''
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship('Teacher')
    '''The main teacher, displayed as contact on event details'''
    
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<Event: type=%s url=%s>' % (self.type.capitalize(), self.url)
    
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
    def link(self):
        '''Link for this event'''
        return link_(self.name, 'events', self.url)
    
    @property
    def breadcrumbs(self):
        '''Array of links for breadcrumb navigation'''
        return [self.link]
    
    @property
    def is_active(self):
        '''If the event is active at the moment'''
        return self.start_time < datetime.now() < self.end_time
    
    @property
    def remaining_time(self):
        '''Remaining time for event'''
        return max(self.end_time - datetime.now(), timedelta(0))
    
    #----------------------------------------------------------------------------
    # Classmethods
    
    @classmethod
    def by_url(cls, url):
        '''Return the event specified by url'''
        return cls.query.filter(cls.url == url).one()
    
#    @classmethod
#    def all_events(cls, only_public=True):
#        '''Return a 3-tuple (current, previous, future) containing all events'''
#        return (cls.current_events(only_public).all(), 
#                cls.previous_events(only_public).all(), 
#                cls.future_events(only_public).all())
    
    @classmethod
    def current_events(cls, only_public=True):
        '''Return a query for currently active events'''
        q = cls.query
        if only_public:
            q = q.filter_by(public=True)
        q = q.filter(cls.start_time < datetime.now()).filter(cls.end_time > datetime.now())
        return q
    
    @classmethod
    def previous_events(cls, only_public=True):
        '''Return a query for previously active events'''
        q = cls.query
        if only_public:
            q = q.filter_by(public=True)
        q = q.filter(cls.end_time < datetime.now())
        return q
    
    @classmethod
    def future_events(cls, only_public=True):
        '''Return a query for future active events'''
        q = cls.query
        if only_public:
            q = q.filter_by(public=True)
        q = q.filter(cls.start_time > datetime.now())
        return q
    

class Course(Event):
    '''An Event with type course'''
    __mapper_args__ = {'polymorphic_identity': 'course'}
    
    def __repr__(self):
        return '<Course: url=%s>' % (self.url)
    

class Contest(Event):
    '''An Event with type contest'''
    __mapper_args__ = {'polymorphic_identity': 'contest'}
    
    def __repr__(self):
        return '<Contest: url=%s>' % (self.url)
    

class Lesson(DeclarativeBase):
    '''A Lesson'''
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(255), nullable=False)
    
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship('Event', backref=backref('lessons'))
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', backref=backref('lessons'))
    
