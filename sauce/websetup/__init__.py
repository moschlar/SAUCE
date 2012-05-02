# -*- coding: utf-8 -*-
"""Setup the SAUCE application

@author: moschlar
"""

import logging

from sauce.config.environment import load_environment

import data

__all__ = ['setup_app']

log = logging.getLogger(__name__)

from schema import setup_schema, teardown_schema
import bootstrap
import data

def setup_app(command, conf, vars):
    """Place any commands to setup sauce here"""
    load_environment(conf.global_conf, conf.local_conf)
    
    setup_schema(command, conf, vars)
    bootstrap.bootstrap(command, conf, vars)
    log.info('Inserting dummy data...')
    
    # Call all *_data functions from the data module
    for d in dir(data):
        if d.endswith('_data'):
            dd = getattr(data, d)
            if callable(dd):
                dd(command,conf,vars)
    
    log.info('Dummy data inserted.')
