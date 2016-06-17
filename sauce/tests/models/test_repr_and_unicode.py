# -*- coding: utf-8 -*-
'''
Test that all model classes have working repr and unicode methods

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

from sauce import model

__all__ = ['test_repr']


entities = [x for x in model.__dict__.itervalues()
    if isinstance(x, type) and issubclass(x, model.DeclarativeBase)]


def _test_repr(entity):
    print repr(entity())


def test_repr():
    for entity in entities:
        yield _test_repr, entity


#TODO
# def _test_unicode(entity):
#     print unicode(entity())
#
#
# def test_unicode():
#     for entity in entities:
#         yield _test_unicode, entity
