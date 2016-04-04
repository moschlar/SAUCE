# -*- coding: utf-8 -*-
"""Setup the SAUCE application

@author: moschlar
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

import logging

from sauce.config.environment import load_environment

from sauce.websetup import schema, bootstrap

__all__ = ['setup_app']

log = logging.getLogger(__name__)


def setup_app(command, conf, vars):  # pylint:disable=redefined-builtin
    """Place any commands to setup SAUCE here"""
    load_environment(conf.global_conf, conf.local_conf)
    schema.setup_schema(command, conf, vars)
    bootstrap.bootstrap(command, conf, vars)
