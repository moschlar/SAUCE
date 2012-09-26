# -*- coding: utf-8 -*-
'''Assignment model module

@author: moschlar
'''

from datetime import datetime, timedelta

from sqlalchemy import Column, ForeignKey, Table, or_, and_, UniqueConstraint
from sqlalchemy.types import Integer, Unicode, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase, metadata, DBSession, curr_prev_future
from sauce.lib.helpers import link
from sauce.model.submission import Submission

# secondary table for many-to-many relation
language_to_assignment = Table('language_to_assignment', metadata,
    Column('language_id', Integer, ForeignKey('languages.id'), primary_key=True),
    Column('assignment_id', Integer, ForeignKey('assignments.id'), primary_key=True)
)

class Assignment(DeclarativeBase):
    __tablename__ = 'assignments'
    
    id = Column(Integer, primary_key=True)
    
    assignment_id = Column(Integer, nullable=False, index=True)
    '''The assignment_id specific to the parent sheet'''
    
    _url = Column('url', String(255))
    '''Not used right now!'''
    
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(65536))
    
    event_id = Column(Integer, ForeignKey('events.id'))
    _event = relationship('Event', backref=backref('assignments'))
    
    _start_time = Column('start_time', DateTime)
    _end_time = Column('end_time', DateTime)
    
    timeout = Column(Float)
    
    allowed_languages = relationship('Language', secondary=language_to_assignment)
    
    show_compiler_msg = Column(Boolean, nullable=False, default=False)
    
    teacher_id = Column(Integer, ForeignKey('users.id'))
    _teacher = relationship('User',
        #backref=backref('assignments')
        )
    
    sheet_id = Column(Integer, ForeignKey('sheets.id'))
    sheet = relationship('Sheet', backref=backref('assignments'))
    
    public = Column(Boolean, nullable=False, default=False)
    '''Whether this Sheet is shown to non-logged in users and non-enrolled students'''
    
    __mapper_args__ = {'order_by': [_end_time, _start_time, _url, assignment_id]}
    __table_args__ = (UniqueConstraint(sheet_id, assignment_id),)
    
    def __unicode__(self):
        return self.name
    
    #----------------------------------------------------------------------------
    # Properties
    
    @property
    def url(self):
        return self.sheet.url + '/assignments/%s' % self.assignment_id
    
    @property
    def link(self):
        '''Link for this Assignment'''
        return link(self.name, self.url)
    
    @property
    def breadcrumbs(self):
        '''Array of links for breadcrumb navigation'''
        return self.sheet.breadcrumbs + [self.link]
    
    @property
    def parent(self):
        return self.sheet
    
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
    def invisible_tests(self):
        return [test for test in self.tests if not test.visible]
    
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

    def submissions_by_user(self, user, team=False):
        ids = [user.id]
        if team:
            try:
                teams = set((t for l in self.sheet.event.lessons for t in l.teams)) & set(user.teams)
                for team in teams:
                    ids.extend((u.id for u in team.members))
            except:
                pass
        return Submission.query.filter_by(assignment_id=self.id).filter(Submission.user_id.in_(ids)).order_by(Submission.user_id)

    #----------------------------------------------------------------------------
    # Classmethods
    
    @classmethod
    def by_assignment_id(cls, assignment_id, sheet):
        return cls.query.filter(cls.sheet_id == sheet.id).filter(cls.assignment_id == assignment_id).one()
    

class Sheet(DeclarativeBase):
    '''A Sheet'''
    __tablename__ = 'sheets'
    
    id = Column(Integer, primary_key=True)
    
    sheet_id = Column(Integer, nullable=False, index=True)
    '''The sheet_id specific to the parent event'''
    
    _url = Column('url', String(255))
    '''Not used right now!'''
    
    name = Column(Unicode(255), nullable=False)
    description = Column(Unicode(65536))
    
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship("Event", backref=backref('sheets'))
    
    _start_time = Column('start_time', DateTime)
    _end_time = Column('end_time', DateTime)
    
    teacher_id = Column(Integer, ForeignKey('users.id'))
    teacher = relationship('User',
        #backref=backref('sheets')
        )
    '''The Teacher that created this sheet'''
    
    public = Column(Boolean, nullable=False, default=False)
    '''Whether this Sheet is shown to non-logged in users and non-enrolled students'''
    
    __mapper_args__ = {'order_by': [_end_time, _start_time, _url, sheet_id]}
    __table_args__ = (UniqueConstraint('event_id', 'sheet_id'),)
    
    def __unicode__(self):
        return self.name
    
    #----------------------------------------------------------------------------
    # Properties
    
    @property
    def url(self):
        return self.event.url + '/sheets/%s' % self.sheet_id
    
    @property
    def link(self):
        '''Link for this Sheet'''
        return link(self.name, self.url)
    
    @property
    def breadcrumbs(self):
        '''Array of links for breadcrumb navigation'''
        return self.event.breadcrumbs + [self.link]
    
    @property
    def parent(self):
        return self.event
    
    @property
    def children(self):
        return self.assignments
    
    @property
    def start_time(self):
        return self._start_time or self.event.start_time
    
    @property
    def end_time(self):
        return self._end_time or self.event.end_time
    
    @property
    def is_active(self):
        '''If the Sheet is active at the moment'''
        return self.start_time < datetime.now() < self.end_time
    
    @property
    def remaining_time(self):
        '''Remaining time for Sheet'''
        return max(self.end_time - datetime.now(), timedelta(0))
    
    #----------------------------------------------------------------------------
    # Classmethods
    
    @classmethod
    def by_sheet_id(cls, sheet_id, event):
        return cls.query.filter(cls.event_id == event.id).filter(cls.sheet_id == sheet_id).one()
#    
#    @classmethod
#    def by_url(cls, url):
#        return cls.query.filter(cls.url == url).one()
#    
#    @classmethod
#    def all_sheets(cls, event=None, only_public=True):
#        '''Return a 3-tuple (current, previous, future) containing all sheets'''
#        return curr_prev_future(cls.current_sheets(event, only_public), 
#                cls.previous_sheets(event, only_public), 
#                cls.future_sheets(event, only_public))
#    
#    @classmethod
#    def current_sheets(cls, event=None, only_public=True):
#        '''Return currently active sheets'''
#        q = cls.query
#        if event:
#            q = q.filter_by(event_id=event.id)
#        if only_public:
#            q = q.filter_by(public=True)
#        return [s for s in q.all() if s.start_time < datetime.now() and s.end_time > datetime.now()]
#        q = q.filter(cls.start_time < datetime.now()).filter(cls.end_time > datetime.now())
#        q = q.filter(or_(
#                         and_(cls._start_time != None, cls._end_time != None, 
#                              cls._start_time < datetime.now(), cls._end_time > datetime.now()),
#                         and_(datetime.now() > DBSession.query(Event.start_time).filter(Event.id==event.id).scalar(),
#                              datetime.now() < DBSession.query(Event.end_time).filter(Event.id==event.id).scalar())
#                         ))
#        return q.all()
#    
#    @classmethod
#    def previous_sheets(cls, event=None, only_public=True):
#        '''Return a query for previously active sheets'''
#        q = cls.query
#        if event:
#            q = q.filter_by(id=event.id)
#        if only_public:
#            q = q.filter_by(public=True)
#        return [s for s in q.all() if datetime.now() > s.end_time]
#        #q = q.filter(cls.end_time < datetime.now())
#        
#    
#    @classmethod
#    def future_sheets(cls, event=None, only_public=True):
#        '''Return a query for future active sheets'''
#        q = cls.query
#        if event:
#            q = q.filter_by(id=event.id)
#        if only_public:
#            q = q.filter_by(public=True)
#        return [s for s in q.all() if s.start_time > datetime.now()]
#        #q = q.filter(cls.start_time > datetime.now())
#    


