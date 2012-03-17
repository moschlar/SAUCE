'''
Created on 13.03.2012

@author: moschlar
'''

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String, Text, Enum
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase

class Event(DeclarativeBase):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    type = Column(Enum('course', 'contest'))
    name = Column(String)
    
    description = Column(Text)
    
    __mapper_args__ = {'polymorphic_on': type}
    
    def __init__(self):
        raise Exception('Do not instantiate plain Event objects, they are useless')
    
    def __repr__(self):
        return '<Event: "%s">' % self.name

class Course(Event):
    __mapper_args__ = {'polymorphic_identity': 'course'}
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", backref=backref('courses'))
    
    def __init__(self, name, teacher=None):
        self.name = name
        if teacher:
            self.teacher = teacher
    
    def __repr__(self):
        return '<Course: "%s">' % self.name

class Contest(Event):
    __mapper_args__ = {'polymorphic_identity': 'contest'}
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Contest: "%s">' % self.name
    
    def __unicode__(self):
        return u'%s' % (self.name)
