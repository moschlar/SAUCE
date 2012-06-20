# -*- coding: utf-8 -*-
"""Setup the SAUCE application

@author: moschlar
"""

import logging

from sauce.config.environment import load_environment

__all__ = ['setup_app']

log = logging.getLogger(__name__)

from schema import setup_schema
import bootstrap

def setup_app(command, conf, vars):
    """Place any commands to setup sauce here"""
    load_environment(conf.global_conf, conf.local_conf)
    
    setup_schema(command, conf, vars)
    bootstrap.bootstrap(command, conf, vars)
    log.info('Inserting dummy data...')
    from data import course_data
    course_data(command, conf, vars)
    log.info('Dummy data inserted.')
