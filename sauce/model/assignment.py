# -*- coding: utf-8 -*-
'''Assignment model module'''

from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey, Table, or_, and_
from sqlalchemy.types import Integer, Unicode, Boolean, Float, DateTime
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase, metadata, DBSession, curr_prev_future
from sauce.model.event import Event


class Sheet(DeclarativeBase):
    __tablename__ = 'sheets'
    __mapper_args__ = {}
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(65536))
    
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship("Event", backref=backref('sheets'))
    
    _start_time = Column('start_time', DateTime)
    _end_time = Column('end_time', DateTime)
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher = relationship('Teacher', backref=backref('sheets'))
    
    public = Column(Boolean, nullable=False, default=False)
    
    def __unicode__(self):
        return self.name
    
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
    
    @classmethod
    def all_sheets(cls, event=None, only_public=True):
        '''Return a 3-tuple (current, previous, future) containing all sheets'''
        return curr_prev_future(cls.current_sheets(event, only_public), 
                cls.previous_sheets(event, only_public), 
                cls.future_sheets(event, only_public))
    
    @classmethod
    def current_sheets(cls, event=None, only_public=True):
        '''Return currently active sheets'''
        q = cls.query
        if event:
            q = q.filter_by(id=event.id)
        if only_public:
            q = q.filter_by(public=True)
        #return [s for s in q.all() if s.start_time < datetime.now() < s.end_time]
        #q = q.filter(cls.start_time < datetime.now()).filter(cls.end_time > datetime.now())
        q = q.filter(or_(
                         and_(cls._start_time != None, cls._end_time != None, 
                              cls._start_time < datetime.now(), cls._end_time > datetime.now()),
                         and_(datetime.now() > DBSession.query(Event.start_time).filter(Event.id==event.id).scalar(),
                              datetime.now() < DBSession.query(Event.end_time).filter(Event.id==event.id).scalar())
                         ))
        return q.all()
    
    @classmethod
    def previous_sheets(cls, event=None, only_public=True):
        '''Return a query for previously active sheets'''
        q = cls.query
        if event:
            q = q.filter_by(id=event.id)
        if only_public:
            q = q.filter_by(public=True)
        return [s for s in q.all() if datetime.now() > s.end_time]
        #q = q.filter(cls.end_time < datetime.now())
        
    
    @classmethod
    def future_sheets(cls, event=None, only_public=True):
        '''Return a query for future active sheets'''
        q = cls.query
        if event:
            q = q.filter_by(id=event.id)
        if only_public:
            q = q.filter_by(public=True)
        return [s for s in q.all() if s.start_time > datetime.now()]
        #q = q.filter(cls.start_time > datetime.now())
    

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
    
    event_id = Column(Integer, ForeignKey('events.id'))
    _event = relationship('Event', backref=backref('assignments'))
    
    _start_time = Column('start_time', DateTime)
    _end_time = Column('end_time', DateTime)
    
    timeout = Column(Float)
    
    allowed_languages = relationship('Language', secondary=language_to_assignment)
    
    show_compiler_msg = Column(Boolean, nullable=False, default=False)
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    _teacher = relationship('Teacher', backref=backref('assignments'))
    
    sheet_id = Column(Integer, ForeignKey('sheets.id'))
    sheet = relationship('Sheet', backref=backref('assignments'))
    
    public = Column(Boolean, nullable=False, default=False)
    
    def __unicode__(self):
        return self.name
    
    @property
    def event(self):
        return self._event or self.sheet.event
    
    @property
    def teacher(self):
        return self._teacher or self.sheet.teacher
    
    @property
    def visible_tests(self):
        return [test for test in self.tests if test.visible]
    
    @property
    def start_time(self):
        if self._start_time:
            return self._start_time
        elif self.sheet:
            return self.sheet.start_time
        elif self.event:
            return self.event.start_time
        raise Exception('No start_time')
    
    @property
    def end_time(self):
        if self._end_time:
            return self._end_time
        elif self.sheet:
            return self.sheet.end_time
        elif self.event:
            return self.event.end_time
        raise Exception('No end_time')
    
    @property
    def is_active(self):
        return self.start_time < datetime.now() < self.end_time
    
    @property
    def remaining_time(self):
        return max(self.end_time - datetime.now(), timedelta(0))


