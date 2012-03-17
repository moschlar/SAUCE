'''
Created on 13.03.2012

@author: moschlar
'''

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String, Text
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
    
    title = Column(String)
    description = Column(Text)
    
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", backref=backref('assignments'))
    
    timeout = Column(Integer)
    
    allowed_languages = relationship('Language', secondary=language_to_assignment)
    
    def __init__(self, title, description='', timeout=1):
        self.title = title
        self.description = description
        self.timeout = timeout
    
    def __repr__(self):
        return '<Assignment "%s">' % self.title
    
    def _get_visible_tests(self):
        return [test for test in self.tests if test.visible]
    visible_tests = property(_get_visible_tests)