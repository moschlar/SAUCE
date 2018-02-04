# -*- coding: utf-8 -*-
"""Drop all tables"""
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2018 Moritz Schlarb
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
from tg import config
import transaction

from sauce.websetup.schema import teardown_schema


if __name__ == "tgshell":
    teardown_schema(None, None, None)
