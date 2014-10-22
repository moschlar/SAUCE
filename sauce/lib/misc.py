# -*- coding: utf-8 -*-
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


def merge(dict1, dict2):
    '''Merge two dicts and join collections

    You can force an entry from dict2 taking full precedence
    (overwriting the corresponding entry from dict1 without
    joining the content) by suffixing the key with '!'.

    :type dict1: dict
    :type dict2: dict
    :rtype: dict
    '''
    result = {}

    for k in set(dict1) - set(dict2):
        result[k] = dict1[k]

    for k in set(dict1) & set(dict2):
        assert type(dict1[k]) == type(dict2[k])
        if isinstance(dict1[k], (list, tuple)):
            result[k] = dict1[k] + dict2[k]
        elif isinstance(dict1[k], dict):
            result[k] = dict1[k].copy()
            result[k].update(dict2[k])
        elif isinstance(dict1[k], set):
            result[k] = dict1[k] | dict2[k]
        else:
            result[k] = dict2[k]

    for k in set(dict2) - set(dict1):
        result[k] = dict2[k]
        if k[-1] == '!':
            result[k[:-1]] = dict2[k]

    return result
