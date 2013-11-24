# -*- coding: utf-8 -*-
'''
Created on Nov 20, 2013

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

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from sauce.lib.misc import merge


class TestMerge(TestCase):

    def test_good(self):
        dict1 = {
            'str': 'xxx',
            'str1': 'abc',
            'l': [1, 2, 3],
            't': ('a', 'b', 'c'),
            's': set(('1', '2', '3')),
            'd': {'a': 1, 'b': 2, 'c': 3, 'x': 42},
        }
        dict2 = {
            'str': 'zzz',
            'str2': 'def',
            'l': [4, 5, 6],
            't': ('d', 'e', 'f'),
            's': set(('4', '5', '6')),
            'd': {'d': 4, 'e': 5, 'f': 6, 'x': 1337},
        }
        merged_dict = merge(dict1, dict2)
        expected_dict = {
            'str': 'zzz',
            'str1': 'abc',
            'str2': 'def',
            'l': [1, 2, 3, 4, 5, 6],
            't': ('a', 'b', 'c', 'd', 'e', 'f'),
            's': set(('1', '2', '3', '4', '5', '6')),
            'd': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'x': 1337},
        }
        self.assertDictEqual(merged_dict, expected_dict)
        