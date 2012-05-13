# -*- coding: utf-8 -*-
'''Person model module

@author: moschlar
'''

import os
import logging
from datetime import datetime
from hashlib import sha256
import string
from random import choice, seed

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime, Enum
from sqlalchemy.orm import relationship, backref, synonym

from sauce.model import DeclarativeBase, metadata, DBSession

log = logging.getLogger(__name__)
chars = string.letters + string.digits + '.!@'

def random_password(length=8):
    password = u''
    for i in xrange(length):
        password += choice(chars)
    return password

class User(DeclarativeBase):
    """
    User definition.

    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.

    """
    __tablename__ = 'users'

    #{ Columns

    id = Column(Integer, autoincrement=True, primary_key=True)

    user_name = Column(Unicode(16), unique=True, nullable=False)

    email_address = Column(Unicode(255), unique=True, nullable=False,
                           info={'rum': {'field':'Email'}})

    display_name = Column(Unicode(255))
    last_name = Column(Unicode(255))
    first_name = Column(Unicode(255))

    _password = Column('password', Unicode(128),
                       info={'rum': {'field':'Password'}})

    created = Column(DateTime, default=datetime.now)
    
    type = Column(Enum('student', 'teacher'))
    
    __mapper_args__ = {'polymorphic_on': type}
    
    #{ Special methods

    def __repr__(self):
        return ('<User: name=%s, email=%s, display=%s>' % (
                self.user_name, self.email_address, self.display_name)).encode('utf-8')

    def __unicode__(self):
        return self.display_name or self.user_name

    #{ Getters and setters

    @property
    def permissions(self):
        """Return a set with all permissions granted to the user."""
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter_by(email_address=email).first()

    @classmethod
    def by_user_name(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter_by(user_name=username).first()

    @classmethod
    def _hash_password(cls, password):
        # Make sure password is a str because we cannot hash unicode objects
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        salt = sha256()
        salt.update(os.urandom(60))
        hash = sha256()
        hash.update(password + salt.hexdigest())
        password = salt.hexdigest() + hash.hexdigest()
        # Make sure the hashed password is a unicode object at the end of the
        # process because SQLAlchemy _wants_ unicode objects for Unicode cols
        if not isinstance(password, unicode):
            password = password.decode('utf-8')
        return password

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    #}

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hash = sha256()
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        hash.update(password + str(self.password[:64]))
        return self.password[64:] == hash.hexdigest()

    def generate_password(self, length=8):
        password = random_password(length)
        self.password = password
        log.debug('New password for %s: %s' % (self.user_name, password))
        return password

# secondary table for many-to-many relation
student_to_team = Table('student_to_team', metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
)

# secondary table for many-to-many relation
student_to_lesson = Table('student_to_lesson', metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('lesson_id', Integer, ForeignKey('lessons.id'), primary_key=True),
)

class Student(User):
    __tablename__ = 'students'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    teams = relationship('Team', secondary=student_to_team, backref=backref('students'))
    _lessons = relationship('Lesson', secondary=student_to_lesson, backref=backref('_students'))
    
    __mapper_args__ = {'polymorphic_identity': 'student'}
    
# Not usable since student may have no team
#    def team_by_event(self, event):
#        teams = []
#        for team in self.teams:
#            if event in team.events:
#                teams.append(team)
#        if len(teams) == 1:
#            return teams[0]
#        else:
#            raise Exception('Damn Hackers!')
#            return None
    @property
    def lessons(self):
        lessons = set(self._lessons)
        for team in self.teams:
            lessons.add(team.lesson)
        return lessons

# secondary table for many-to-many relation
#teacher_to_event = Table('teacher_to_event', metadata,
#    Column('teacher_id', Integer, ForeignKey('teachers.id'), primary_key=True),
#    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
#)

class Teacher(User):
    __tablename__ = 'teachers'
    
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {'polymorphic_identity': 'teacher'}

class Team(DeclarativeBase):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(Unicode(255), nullable=False)
    
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    lesson = relationship('Lesson', backref=backref('teams'))
    
    @property
    def event(self):
        return self.lesson.event
    
    @property
    def submissions(self):
        return [submission for student in self.students for submission in student.submissions]

