# -*- coding: utf-8 -*-
"""Setup the SAUCE application

@author: moschlar
"""

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
    """Place any commands to setup sauce here"""
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
    if run_tests:
        log.info('Running test cases for half the submissions...')
        q = model.DBSession.query(model.Submission)
        for submission in sample(q.all(), q.count() / 2):
            submission.run_tests()
        transaction.commit()
