# -*- coding: utf-8 -*-
'''Event model module'''

from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, Enum, DateTime
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase

class Event(DeclarativeBase):
    __tablename__ = 'events'
    __mapper_args__ = {'order_by': ['end_time', 'start_time']}
    
    id = Column(Integer, primary_key=True)
    type = Column(Enum('course', 'contest'), nullable=False)
    
    name = Column(Unicode(255), nullable=False)
    
    description = Column(Unicode(65536))
    
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime, nullable=False, default=datetime.now)
    
    password = Column(Unicode(255))
    '''The password students have to enter in order to enroll to an event'''
    
    #teacher_id = Column(Integer, ForeignKey('teachers.id'))
    #teacher = relationship('Teacher', backref=backref('events'))
    
    __mapper_args__ = {'polymorphic_on': type, 'order_by': ['end_time', 'start_time']}
    
    def __unicode__(self):
        return self.name
    
    @property
    def is_active(self):
        return self.start_time < datetime.now() < self.end_time
    
    @property
    def remaining_time(self):
        return max(self.end_time - datetime.now(), timedelta(0))

class Course(Event):
    __mapper_args__ = {'polymorphic_identity': 'course'}
    

class Contest(Event):
    __mapper_args__ = {'polymorphic_identity': 'contest'}
    

class Lesson(DeclarativeBase):
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(255), nullable=False)
    
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship('Event', backref=backref('lessons'))
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', backref=backref('lessons'))
    
