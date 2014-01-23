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

import os
import logging

from random import sample

import transaction
from paste.deploy.converters import asbool

from schema import setup_schema
from bootalchemy.loader import Loader, YamlLoader

from sauce.config.environment import load_environment
from sauce import model

__all__ = ['setup_app']

log = logging.getLogger(__name__)


def setup_app(command, conf, vars):
    """Place any commands to setup SAUCE here"""
    load_environment(conf.global_conf, conf.local_conf)

    setup_schema(command, conf, vars)

    loader = YamlLoader(model)

    for filename in sorted(os.listdir(os.path.dirname(__file__) + '/data')):
        if filename.endswith('.yaml'):
            name = filename.lstrip('01234567890').replace('.yaml', '')
            log.info('Inserting %s data...' % name)
            loader.loadf(model.DBSession, '%s/data/%s' % (os.path.dirname(__file__), filename))
    transaction.commit()

    run_tests = asbool(conf.get('websetup.run_tests', True))

    if run_tests:  # pragma: no cover
        log.info('Running test cases for half the submissions...')
        q = model.DBSession.query(model.Submission)
        for submission in sample(q.all(), q.count() / 2):
            submission.run_tests()
        transaction.commit()
