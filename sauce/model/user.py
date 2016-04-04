# -*- coding: utf-8 -*-
'''Person model module

@author: moschlar
'''
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import os
import string
from datetime import datetime
from hashlib import sha256
from random import choice
from warnings import warn

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship, synonym
from sqlalchemy.types import DateTime, Enum, Integer, Unicode
from webhelpers.html.tools import mail_to

from sauce.model import DBSession, DeclarativeBase, metadata


__all__ = ('User', 'Team')


log = logging.getLogger(__name__)

PASSWORD_CHARS = string.letters + string.digits + '.!@'


def random_password(length=8):
    return ''.join((choice(PASSWORD_CHARS) for _ in xrange(length)))


class User(DeclarativeBase):
    """
    User definition.

    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.
    """
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_name = Column(Unicode(255), nullable=False, unique=True, index=True)
    email_address = Column(Unicode(255), nullable=False, unique=False, index=True)

    _last_name = Column('last_name', Unicode(255), nullable=True)
    _first_name = Column('first_name', Unicode(255), nullable=True)
    _display_name = Column('display_name', Unicode(255), nullable=True)

    @hybrid_property
    def display_name(self):
        if self._display_name:
            return self._display_name
        if self._last_name and self._first_name:
            return u'%s, %s' % (self._last_name, self._first_name)
        elif self._last_name:
            return self._last_name
        elif self._first_name:
            return self._first_name
        else:
            return u''

    @display_name.setter
    def display_name(self, name):
        self._display_name = name
        try:
            if ',' in name:
                (last, first) = name.split(',', 1)
            else:
                (first, last) = name.rsplit(' ', 1)
            self._first_name = first
            self._last_name = last
        except (ValueError, TypeError):
            self._first_name = None
            self._last_name = None

    _password = Column('password', Unicode(128), nullable=True)

    created = Column(DateTime, nullable=True, default=datetime.now)

    __mapper_args__ = {'order_by': [user_name]}

    def __repr__(self):
        return (u'<User: id=%r, user_name=%r>'
            % (self.id, self.user_name)
        ).encode('utf-8')

    def __unicode__(self):
        return self.display_name or self.user_name

    def __str__(self):
        return unicode(self).encode('utf-8')

    @property
    def link(self):
        return mail_to(self.email_address, self.display_name, subject=u'[SAUCE] ')

    @property
    def permissions(self):
        """Return a set with all permissions granted to the user."""
        perms = set()
        for g in self.groups:
            perms |= set(g.permissions)
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
        hash = sha256()  # pylint:disable=redefined-builtin
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
        if not self.password:
            # Empty passwords are possible, but login will never work then.
            return False
        hash = sha256()  # pylint:disable=redefined-builtin
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        #TODO: Check if this str() can be replaced by unicode()
        hash.update(password + str(self.password[:64]))
        return self.password[64:] == hash.hexdigest()

    def generate_password(self, length=8):
        password = random_password(length)
        self.password = password
        log.info('New password for %r: %s', self, password)
        return password

    # Additional properties that were in Student before

    @property
    def lessons(self):
        lessons = set(self._lessons)
        for team in self.teams:
            lessons.add(team.lesson)
        return lessons

    @property
    def teammates(self):
        return [s for t in self.teams for s in t.members if s != self]

    def teammates_in_lesson(self, lesson):
        return [s for t in self.teams for s in t.members if t.lesson == lesson and s != self]

    def teammates_in_event(self, event):
        return [s for t in self.teams for s in t.members if t.lesson in event.lessons and s != self]

# secondary table for many-to-many relation
team_members = Table('team_members', metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
)

# secondary table for many-to-many relation
lesson_members = Table('lesson_members', metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('lesson_id', Integer, ForeignKey('lessons.id'), primary_key=True),
)

# secondary table for many-to-many relation
event_members = Table('event_members', metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
)


class Team(DeclarativeBase):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Unicode(255), nullable=False)

    members = relationship('User', secondary=team_members,
        backref=backref('teams', order_by=name),
        order_by='User.user_name')

    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False, index=True)
    lesson = relationship('Lesson',
        backref=backref('teams',
            order_by=name,
            cascade='all, delete-orphan')
    )

    __mapper_args__ = {'order_by': [lesson_id, name]}

    def __repr__(self):
        return (u'<Team: id=%r, lesson_id=%r, name=%r>'
            % (self.id, self.lesson_id, self.name)
        ).encode('utf-8')

    def __unicode__(self):
        return u'Team "%s"' % self.name

    def __contains__(self, item):
        return item in self.members

    @property
    def event(self):
        return self.lesson.event

    @property
    def submissions(self):
        return [submission for user in self.members for submission in user.submissions]

    @property
    def users(self):  # pragma: no cover
        warn('Team.users', DeprecationWarning, stacklevel=2)
        return self.members

    @property
    def students(self):  # pragma: no cover
        warn('Team.students', DeprecationWarning, stacklevel=2)
        return self.members

    def rename(self, *args, **kwargs):
        '''Rename the Team with its member usernames'''
        self.name = '-'.join(u.user_name for u in self.members)
        return self.name
