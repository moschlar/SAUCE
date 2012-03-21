'''
Created on 13.03.2012

@author: moschlar
'''

from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer, Unicode, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase

class Event(DeclarativeBase):
    __tablename__ = 'events'
    __mapper_args__ = {'order_by': ['end_date', 'start_date']}
    
    id = Column(Integer, primary_key=True)
    type = Column(Enum('course', 'contest'), nullable=False)
    
    name = Column(Unicode(255), nullable=False)
    
    description = Column(Unicode)
    
    start_time = Column(DateTime, nullable=False, default=datetime.now)
    end_time = Column(DateTime, nullable=False, default=datetime.now)
    
    __mapper_args__ = {'polymorphic_on': type}
    
#    def __repr__(self):
#        return 'Event("%s")' % self.name
    
    def __str__(self):
        return '%s' % (self.name)

    def __unicode__(self):
        return '%s' % (self.name)
    
    @property
    def is_active(self):
        return self.start_time < datetime.now() < self.end_time
    
    @property
    def remaining_time(self):
        return max(self.end_time - datetime.now(), timedelta(0))

class Course(Event):
    __mapper_args__ = {'polymorphic_identity': 'course'}
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", backref=backref('courses'))
    
#    def __init__(self, name, teacher=None):
#        self.name = name
#        if teacher:
#            self.teacher = teacher
#    
#    def __repr__(self):
#        return 'Course("%s")' % self.name

class Contest(Event):
    __mapper_args__ = {'polymorphic_identity': 'contest'}
    
#    def __init__(self, name):
#        self.name = name
    
#    def __repr__(self):
#        return 'Contest("%s")' % self.name
    
#    def __unicode__(self):
#        return u'%s' % (self.name)
