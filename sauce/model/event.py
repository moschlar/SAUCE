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
    
    description = Column(Unicode)
    
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime, nullable=False, default=datetime.now)
    
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
    

