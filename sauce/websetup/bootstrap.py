# -*- coding: utf-8 -*-
"""Setup the SAUCE application"""
import os
import logging
import transaction
from random import sample
from paste.deploy.converters import asbool
from bootalchemy.loader import Loader, YamlLoader
from sauce import model


log = logging.getLogger(__name__)


def bootstrap(command, conf, vars):
    """Place any commands to setup sauce here"""

    # <websetup.bootstrap.before.auth>
    from sqlalchemy.exc import IntegrityError
    try:
        loader = YamlLoader(model)

        for filename in sorted(os.listdir(os.path.dirname(__file__) + '/data')):
            if filename.endswith('.yaml'):
                name = filename.lstrip('01234567890').replace('.yaml', '')
                log.info('Inserting %s data...', name)
                loader.loadf(model.DBSession, '%s/data/%s' % (os.path.dirname(__file__), filename))
        transaction.commit()

        run_tests = asbool(conf.get('websetup.run_tests', True))

        if run_tests:  # pragma: no cover
            log.info('Running test cases for half the submissions...')
            q = model.DBSession.query(model.Submission)
            for submission in sample(q.all(), q.count() / 2):
                submission.run_tests()
            transaction.commit()
    except IntegrityError:
        log.warn('Warning, there was a problem adding your data, '
              'it may have already been added:', exc_info=True)
        transaction.abort()
        log.info('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
