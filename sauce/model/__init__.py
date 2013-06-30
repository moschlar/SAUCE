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
from collections import namedtuple

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy import event as _event
from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Enum

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
#metadata2 = MetaData()

#####
# Generally you will not want to define your table's mappers, and data objects
# here in __init__ but will want to create modules them in the model directory
# and import them at the bottom of this file.
#
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

    #global t_reflected

    #t_reflected = Table("Reflected", metadata,
    #    autoload=True, autoload_with=engine)

    #mapper(Reflected, t_reflected)


curr_prev_future = namedtuple('curr_prev_future', ['current', 'previous', 'future'])

visibility_type = Enum(u'anonymous', u'users', u'students', u'tutors', u'teachers', name='visibility_type')

# Import your model modules here.
from sauce.model.auth import Group, Permission

from sauce.model.assignment import Assignment, Sheet
from sauce.model.event import Event, Contest, Course, Lesson
from sauce.model.language import Language, Compiler, Interpreter
from sauce.model.submission import Submission, Judgement
from sauce.model.test import Test, Testrun
from sauce.model.news import NewsItem
#from sauce.model.discussion import Discussion
from sauce.model.user import User, Team


# Event listeners for keeping the data healthy


def lesson_team_members(session, flush_context, instances):
    try:
        for obj in session.dirty:
            if isinstance(obj, User):
                for t in obj.teams:
                    if t.lesson in obj._lessons:
                        log.info('Automatically removing %s from %s because of %s', obj, t.lesson, t)
                        obj._lessons.remove(t.lesson)
    except:
        log.exception('lesson_team_members failed')

_event.listen(DBSession, 'before_flush', lesson_team_members)
