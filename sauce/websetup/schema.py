# -*- coding: utf-8 -*-
"""Setup the SAUCE application"""

import logging
from tg import config
import transaction

log = logging.getLogger(__name__)

def setup_schema(command, conf, vars):
    """Place any commands to setup sauce here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from sauce import model

    # <websetup.websetup.schema.after.model.import>

    engine = config['pylons.app_globals'].sa_engine
    
    # <websetup.websetup.schema.before.metadata.create_all>
    log.info("Creating tables")
    model.metadata.create_all(bind=engine)

    # <websetup.websetup.schema.after.metadata.create_all>
    transaction.commit()

    log.info('Initializing Migrations')
    import alembic.config, alembic.command
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("script_location", "migration")
    alembic_cfg.set_main_option("sqlalchemy.url", config['sqlalchemy.url'])
    alembic.command.stamp(alembic_cfg, "head")

def teardown_schema(command, conf, vars):
    
    from sauce import model
    
    engine = config['pylons.app_globals'].sa_engine
    
    log.info("Dropping tables")
    model.metadata.drop_all(bind=engine)
    
    transaction.commit()