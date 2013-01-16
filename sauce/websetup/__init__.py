# -*- coding: utf-8 -*-
"""Setup the SAUCE application

@author: moschlar
"""

import os
import logging

import transaction
from sqlalchemy.exc import IntegrityError

from schema import setup_schema
#import bootstrap
from bootalchemy.loader import Loader, YamlLoader

from sauce.config.environment import load_environment
from sauce import model

__all__ = ['setup_app']

log = logging.getLogger(__name__)


def setup_app(command, conf, vars):
    """Place any commands to setup sauce here"""
    load_environment(conf.global_conf, conf.local_conf)

    setup_schema(command, conf, vars)
    #bootstrap.bootstrap(command, conf, vars)

    log.info('Inserting dummy data...')
    loader = YamlLoader(model)

    for (name, filename) in (
        ('bootstrap', 'bootstrap.yaml'),
        ('language', 'languages.yaml'),
        ('user', 'users.yaml'),
        ('event', 'events.yaml')):
        log.info('Inserting %s data...' % name)
        try:
            loader.loadf(model.DBSession, '%s/data/%s' % (os.path.dirname(__file__), filename))
            transaction.commit()
        except IntegrityError:
            raise
