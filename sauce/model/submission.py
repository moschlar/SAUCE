'''
Created on 13.03.2012

@author: moschlar
'''

from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase

class Submission(DeclarativeBase):
    __tablename__ = 'submissions'
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, nullable=False, default=datetime.now)
    
    source = Column(Text)
    filename = Column(String)
    
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    assignment = relationship("Assignment", backref=backref('submissions'))
    
    language_id = Column(Integer, ForeignKey('languages.id'), nullable=False)
    language = relationship("Language")
    
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    student = relationship("Student", backref=backref('submissions'))
    
#    def __init__(self, assignment, language, student, date=None):
#        self.assignment = assignment
#        self.language = language
#        self.student = student
#        self.date = date or datetime.now()
    
#    def __repr__(self):
#        return 'Submission()'
    
    def __str__(self):
        return 'Submission %s' % (self.id or '')
    
    def __unicode__(self):
        return u'Submission %s' % (self.id or '')
