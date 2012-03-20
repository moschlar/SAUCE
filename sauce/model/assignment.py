'''
Created on 13.03.2012

@author: moschlar
'''

from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String, Text, Boolean, Float, DateTime
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase, metadata

# secondary table for many-to-many relation
language_to_assignment = Table('language_to_assignment', metadata,
    Column('language_id', Integer, ForeignKey('languages.id')),
    Column('assignment_id', Integer, ForeignKey('assignments.id'))
)

class Assignment(DeclarativeBase):
    __tablename__ = 'assignments'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship("Event", backref=backref('assignments'))
    
    _start_time = Column('start_time', DateTime)
    _end_time = Column('end_time', DateTime)
    
    timeout = Column(Float)
    
    allowed_languages = relationship('Language', secondary=language_to_assignment)
    
    show_compiler_msg = Column(Boolean, nullable=False, default=False)
    
#    def __init__(self, title, description='', timeout=1, allowed_languages=[], show_compiler_msg=False):
#        self.title = title
#        self.description = description
#        self.timeout = timeout
#        self.allowed_languages = allowed_languages
#        self.show_compiler_msg = show_compiler_msg
    
#    def __repr__(self):
#        return 'Assignment("%s")' % self.name
    
    @property
    def visible_tests(self):
        return [test for test in self.tests if test.visible]
    
    @property
    def start_time(self):
        if self._start_time:
            return self._start_time
        else:
            return self.event.start_time
    
    @property
    def end_time(self):
        if self._end_time:
            return self._end_time
        else:
            return self.event.end_time
    
    @property
    def is_active(self):
        return self.start_time < datetime.now() < self.end_time
    
    @property
    def remaining_time(self):
        return max(self.end_time - datetime.now(), timedelta(0))
