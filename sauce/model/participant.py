'''
Created on 13.03.2012

@author: moschlar
'''

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase, metadata
from sauce.model.auth import User, Group, Permission

# secondary table for many-to-many relation
participant_to_event = Table('participant_to_event', metadata,
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('team_id', Integer, ForeignKey('teams.id')),
)

class Student(DeclarativeBase):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(255), nullable=False)
    
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team', backref=backref('members'))
    
    _events = relationship('Event', secondary=participant_to_event, backref='member_students')
    
    user_id = Column(Integer, ForeignKey('tg_user.user_id'))
    user = relationship('User', backref=backref('student', uselist=False))
    
#    def __init__(self, name, team=None):
#        self.name = name
#        if team:
#            self.team = team
    
#    def __repr__(self):
#        return 'Student(name="%s")' % self.name
    
    @property
    def events(self):
        if self.team:
            return self._events + self.team.events
        else:
            return self._events
    

class Team(DeclarativeBase):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(255), nullable=False)
    
    events = relationship("Event", secondary=participant_to_event, backref='member_teams')
    
#    def __init__(self, name, members=[]):
#        self.name = name
#        if members:
#            self.members.extend(members)
    
#    def __repr__(self):
#        return 'Team(name="%s")' % self.name

