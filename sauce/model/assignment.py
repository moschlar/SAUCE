# -*- coding: utf-8 -*-
'''Assignment model module'''

from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer, Unicode, Boolean, Float, DateTime
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase, metadata

# secondary table for many-to-many relation
language_to_assignment = Table('language_to_assignment', metadata,
    Column('language_id', Integer, ForeignKey('languages.id'), primary_key=True),
    Column('assignment_id', Integer, ForeignKey('assignments.id'), primary_key=True)
)

class Assignment(DeclarativeBase):
    __tablename__ = 'assignments'
    __mapper_args__ = {'order_by': ['end_time', 'start_time']}
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(65536))
    
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship("Event", backref=backref('assignments'))
    
    _start_time = Column('start_time', DateTime)
    _end_time = Column('end_time', DateTime)
    
    timeout = Column(Float)
    
    allowed_languages = relationship('Language', secondary=language_to_assignment)
    
    show_compiler_msg = Column(Boolean, nullable=False, default=False)
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', backref=backref('assignments'))
    
    def __unicode__(self):
        return self.name
    
    @property
    def visible_tests(self):
        return [test for test in self.tests if test.visible]
    
    @property
    def start_time(self):
        return self._start_time or self.event.start_time

    
    @property
    def end_time(self):
        return self._end_time or self.event.end_time
    
    @property
    def is_active(self):
        return self.start_time < datetime.now() < self.end_time
    
    @property
    def remaining_time(self):
        return max(self.end_time - datetime.now(), timedelta(0))
