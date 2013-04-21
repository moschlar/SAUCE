# -*- coding: utf-8 -*-
'''Language model module

Possible variables in argv command line strings are:

    {path}: Absolute path to temporary working directory
    {basename}: Plain file name without path and extension
    {srcfile}: Filename with source extension
    {binfile}: Filename with binary extension

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

import subprocess
import shlex

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, Float
from sqlalchemy.orm import relationship

from sauce.model import DeclarativeBase


def _cmd(cmd):
    try:
        # Don't care about stdout/stderr, just get all output
        p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (output, _) = p.communicate()
        return unicode(output)
    except:
        return u''


class Compiler(DeclarativeBase):
    __tablename__ = 'compilers'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode(255), nullable=False)

    path = Column(Unicode(255), nullable=False)
    argv = Column(Unicode(255), nullable=False, default=u'{srcfile}')

    version_cmd = Column(Unicode(255), nullable=True, default=u'--version')
    help_cmd = Column(Unicode(255), nullable=True, default=u'--help')

    timeout = Column(Float)

    def __unicode__(self):
        return self.name

    @property
    def version(self):
        if self.version_cmd:
            return _cmd('%s %s' % (self.path, self.version_cmd))
        else:
            return u''

    @property
    def help(self):
        if self.help_cmd:
            return _cmd('%s %s' % (self.path, self.help_cmd))
        else:
            return u''


class Interpreter(DeclarativeBase):
    __tablename__ = 'interpreters'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode(255), nullable=False)

    path = Column(Unicode(255), nullable=False)
    argv = Column(Unicode(255), nullable=False, default=u'{binfile}')

    version_cmd = Column(Unicode(255), nullable=True, default=u'--version')
    help_cmd = Column(Unicode(255), nullable=True, default=u'--help')

    def __unicode__(self):
        return self.name

    @property
    def version(self):
        if self.version_cmd:
            return _cmd('%s %s' % (self.path, self.version_cmd))
        else:
            return u''

    @property
    def help(self):
        if self.help_cmd:
            return _cmd('%s %s' % (self.path, self.help_cmd))
        else:
            return u''


class Language(DeclarativeBase):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)

    name = Column(Unicode(255), nullable=False)

    lexer_name = Column(Unicode(255), nullable=True)
    '''Lexer name for Pygments'''

    extension_src = Column(Unicode(255))
    extension_bin = Column(Unicode(255))

    compiler_id = Column(Integer, ForeignKey('compilers.id'))
    compiler = relationship('Compiler', backref="languages")

    interpreter_id = Column(Integer, ForeignKey('interpreters.id'))
    interpreter = relationship('Interpreter', backref="languages")

    def __unicode__(self):
        return self.name
