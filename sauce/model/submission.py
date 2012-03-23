# -*- coding: utf-8 -*-
'''Submission model module'''

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase

class Submission(DeclarativeBase):
    __tablename__ = 'submissions'
    __mapper_args__ = {'order_by': desc('date')}
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    filename = Column(Unicode(255))
    source = Column(Unicode(10485760))
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship("Assignment", backref=backref('submissions'))
    
    language_id = Column(Integer, ForeignKey('languages.id'), nullable=False)
    language = relationship("Language")
    
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    student = relationship("Student", backref=backref('submissions'))
    
    complete = Column(Boolean, default=False)
    
    testrun_id = Column(Integer, ForeignKey('testruns.id'))
    testrun = relationship('TestRun', backref=backref('submission', uselist=False))
    
    def __unicode__(self):
        return u'Submission %s' % (self.id or '')
    
    @property
    def team(self):
        team = [team for team in self.student.teams if self.assignment.event in team.events]
        if team:
            return team[0]
        else:
            return None
    

