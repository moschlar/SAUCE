'''
Created on 13.03.2012

@author: moschlar
'''

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Integer, String, Text, Float
from sqlalchemy.orm import relationship, backref

from sauce.model import DeclarativeBase

class Compiler(DeclarativeBase):
    __tablename__ = 'compilers'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)
    
    path = Column(String, nullable=False)
    argv = Column(String, nullable=False, default='{srcfile}')
    
    timeout = Column(Float)
    
#    def __init__(self, name, path, argv='', timeout=None):
#        self.name = name
#        self.path = path
#        if argv:
#            self.argv = argv
#        if timeout:
#            self.timeout = timeout
    
#    def __repr__(self):
#        return 'Compiler("%s")' % self.name

class Interpreter(DeclarativeBase):
    __tablename__ = 'interpreters'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)
    
    path = Column(String, nullable=False)
    argv = Column(String, nullable=False, default='{binfile}')
    
#    def __init__(self, name, path, argv=''):
#        self.name = name
#        self.path = path
#        if argv:
#            self.argv = argv
    
#    def __repr__(self):
#        return 'Interpreter("%s")' % self.name


class Language(DeclarativeBase):
    __tablename__ = 'languages'
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)
    extension = Column(String)
    
    compiler_id = Column(Integer, ForeignKey('compilers.id'))
    compiler = relationship('Compiler', backref="languages")
    
    interpreter_id = Column(Integer, ForeignKey('interpreters.id'))
    interpreter = relationship('Interpreter', backref="languages")
    
#    def __init__(self, name, extension=None, compiler=None, interpreter=None):
#        self.name = name
#        if extension:
#            self.extension = extension
#        if compiler:
#            self.compiler = compiler
#        if interpreter:
#            self.interpreter = interpreter
    
#    def __repr__(self):
#        return 'Language("%s")' % self.name
