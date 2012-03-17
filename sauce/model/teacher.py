'''
Created on 13.03.2012

@author: moschlar
'''

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase

class Teacher(DeclarativeBase):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String)