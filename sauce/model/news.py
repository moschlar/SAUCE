# -*- coding: utf-8 -*-
'''News model module'''

from datetime import datetime

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import mapper, relationship, backref
from sqlalchemy.sql import desc

from sauce.model import DeclarativeBase

class NewsItem(DeclarativeBase):
    __tablename__ = 'newsitems'
    __mapper_args__ = {'order_by': desc('date')}
    
    id = Column(Integer, primary_key=True)
    
    date = Column(DateTime, default=datetime.now)
    
    subject = Column(Unicode(255), nullable=False)
    
    message = Column(Unicode(65536))
    
    # if event == None, NewsItem is to be displayed on front page
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', backref=backref('news'))
    

