# -*- coding: utf-8 -*-
'''News model module

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

from datetime import datetime

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase


class NewsItem(DeclarativeBase):
    '''A NewsItem'''
    __tablename__ = 'newsitems'

    id = Column(Integer, primary_key=True)

    date = Column(DateTime, default=datetime.now)

    subject = Column(Unicode(255), nullable=False)

    message = Column(Unicode(64 * 1024))

    event_id = Column(Integer, ForeignKey('events.id'), index=True)
    event = relationship('Event',
        backref=backref('news', order_by=desc(date)),
        doc='If event is None, NewsItem is to be displayed on front page instead of event page'
    )

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User',
        #backref=backref('news',
        #    cascade='all, delete-orphan'),
        doc='The User that wrote the NewsItem'
    )

    public = Column(Boolean, nullable=False, default=True)

    __mapper_args__ = {'order_by': desc(date)}

    def __repr__(self):
        return (u'<NewsItem: id=%r, user_id=%r, event_id=%r, subject=%r>'
            % (self.id, self.user_id, self.event_id, self.subject)
        ).encode('utf-8')

    def __unicode__(self):
        return u'NewsItem %d "%s"' % (self.id or '', self.subject)
