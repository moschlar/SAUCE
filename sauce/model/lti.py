# -*- coding: utf-8 -*-
"""LTI model module.

TODO: Use SQLAlchemy magic on model to make queries on assignment easier
TODO: Tests
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

from sqlalchemy import Column, ForeignKey, Index, Table
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import Integer, Unicode

from sauce.model import DBSession, DeclarativeBase, metadata
from sauce.model.assignment import Assignment
from sauce.model.event import Event


__all__ = ('LTI', )


# secondary table for many-to-many relation
lti_to = Table('lti_to', metadata,
    Column('lti_id', Integer, ForeignKey('lti.id'), primary_key=True),
    Column('assignment_id', Integer, ForeignKey('assignments.id'), nullable=True),
    Column('event_id', Integer, ForeignKey('events.id'), nullable=True),

    Index('idx_lti_assignment', 'lti_id', 'assignment_id', unique=True),
    Index('idx_lti_event', 'lti_id', 'event_id', unique=True),
)


class LTI(DeclarativeBase):
    __tablename__ = 'lti'

    id = Column(Integer, primary_key=True)

    oauth_key = Column(Unicode(255))
    oauth_secret = Column(Unicode(255))

    assignments = relationship(Assignment, secondary=lti_to,
        backref=backref('_lti', uselist=False))
    events = relationship(Event, secondary=lti_to,
        backref=backref('lti', uselist=False))

    def __repr__(self):
        return (u'<LTI: id=%r>'
            % (self.id)
        ).encode('utf-8')

    def __unicode__(self):
        return u'LTI %d' % self.id
