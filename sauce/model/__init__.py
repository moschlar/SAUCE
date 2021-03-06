# -*- coding: utf-8 -*-
"""The application's model objects

@author: moschlar
"""
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

from sqlalchemy import event as _event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension


__all__ = (
    'DBSession', 'DeclarativeBase', 'metadata',
    'Group', 'Permission',
    'Assignment', 'Sheet',
    'Event', 'Contest', 'Course', 'Lesson',
    'Language', 'Compiler', 'Interpreter',
    'LTI',
    'NewsItem',
    'Submission', 'Judgement',
    'Test', 'Testrun',
    'User', 'Team',
)


log = logging.getLogger(__name__)

# Global session manager: DBSession() returns the Thread-local
# session object appropriate for the current web request.
maker = sessionmaker(autoflush=True, autocommit=False, expire_on_commit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

# Base class for all of our model classes: By default, the data model is
# defined with SQLAlchemy's declarative extension, but if you need more
# control, you can switch to the traditional method.
DeclarativeBase = declarative_base()

# There are two convenient ways for you to spare some typing.
# You can have a query property on all your model classes by doing this:
DeclarativeBase.query = DBSession.query_property()
# Or you can use a session-aware mapper as it was used in TurboGears 1:
# DeclarativeBase = declarative_base(mapper=DBSession.mapper)

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata

# If you have multiple databases with overlapping table names, you'll need a
# metadata for each database. Feel free to rename 'metadata2'.
# from sqlalchemy import MetaData
# metadata2 = MetaData()

#####
# Generally you will not want to define your table's mappers, and data objects
# here in __init__ but will want to create modules them in the model directory
# and import them at the bottom of this file.
######


def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)

    # If you are using reflection to introspect your database and create
    # table objects for you, your tables must be defined and mapped inside
    # the init_model function, so that the engine is available if you
    # use the model outside tg2, you need to make sure this is called before
    # you use the model.

    #
    # See the following example:
    #
    # global t_reflected
    # t_reflected = Table("Reflected", metadata,
    #                     autoload=True, autoload_with=engine)
    # mapper(Reflected, t_reflected)


# Import your model modules here.

from sauce.model.assignment import Assignment, Sheet
from sauce.model.auth import Group, Permission
from sauce.model.event import Contest, Course, Event, Lesson
from sauce.model.language import Compiler, Interpreter, Language
from sauce.model.lti import LTI
from sauce.model.news import NewsItem
from sauce.model.submission import Judgement, Submission
from sauce.model.test import Test, Testrun
from sauce.model.user import Team, User


# Event listeners for keeping the data healthy

def _lesson_team_members(session, flush_context, instances):
    '''Remove users as direct members from a lesson when they are in a team for
    that lesson'''
    try:
        for obj in session.dirty:
            if isinstance(obj, User):
                for t in obj.teams:
                    if t.lesson in obj._lessons:
                        log.info('Automatically removing User %r from Lesson %r because of Team %r',
                            obj, t.lesson, t)
                        obj._lessons.remove(t.lesson)
    except:  # pragma: no cover
        log.exception('lesson_team_members failed')

_event.listen(DBSession, 'before_flush', _lesson_team_members)


def _event_lesson_members(session, flush_context, instances):
    '''Remove users as direct members from an event when they are in a team or
    lesson for that event'''
    try:
        for obj in session.dirty:
            if isinstance(obj, User):
                for t in obj.teams:
                    if t.lesson.event in obj._events:
                        log.info('Automatically removing User %r from Event %r because of Team %r',
                            obj, t.lesson.event, t)
                        obj._events.remove(t.lesson.event)
                for l in obj._lessons:
                    if l.event in obj._events:
                        log.info('Automatically removing User %r from Event %r because of Lesson %r',
                            obj, l.event, l)
                        obj._events.remove(l.event)
    except:  # pragma: no cover
        log.exception('event_lesson_members failed')

_event.listen(DBSession, 'before_flush', _event_lesson_members)


def _test_visibility(session, flush_context, instances):
    '''Set old _visible attribute on tests for backwards compatibility'''
    try:
        for obj in session.dirty:
            if isinstance(obj, Test):
                if obj.visibility is not None:
                    obj._visible = obj.visibility == 'visible'
    except:  # pragma: no cover
        log.exception('test_visibility failed')

_event.listen(DBSession, 'before_flush', _test_visibility)
