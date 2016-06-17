# -*- coding: utf-8 -*-
"""Setup the SAUCE application"""
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
from tg import config
import transaction

log = logging.getLogger(__name__)


def setup_schema(command, conf, vars):  # pylint:disable=redefined-builtin
    """Place any commands to setup sauce here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from sauce import model

    # <websetup.websetup.schema.after.model.import>

    engine = config['tg.app_globals'].sa_engine

    # <websetup.websetup.schema.before.metadata.create_all>
    log.info("Creating tables...")
    model.metadata.create_all(bind=engine)

    # <websetup.websetup.schema.after.metadata.create_all>
    transaction.commit()

    log.info('Initializing Migrations...')
    import alembic.config, alembic.command
    alembic_cfg = alembic.config.Config()
    alembic_cfg.set_main_option("script_location", "migration")
    alembic_cfg.set_main_option("sqlalchemy.url", config['sqlalchemy.url'])
    alembic.command.stamp(alembic_cfg, "head")


def teardown_schema(command, conf, vars):  # pylint:disable=redefined-builtin, pragma: no cover

    from sauce import model

    engine = config['tg.app_globals'].sa_engine

    log.info("Dropping tables...")
    model.metadata.drop_all(bind=engine)

    transaction.commit()
