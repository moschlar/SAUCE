# -*- coding: utf-8 -*-
"""Alembic migration environment

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

from __future__ import with_statement
from alembic import context
from paste.deploy import loadapp
from sqlalchemy.engine.base import Engine
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
#fileConfig(config.config_file_name)

#try:
#    # if pylons app already in, don't create a new app
#    from pylons import config as pylons_config
#    pylons_config['__file__']
#except:
#    config = context.config
#    # can use config['__file__'] here, i.e. the Pylons
#    # ini file, instead of alembic.ini
#    config_file = config.get_main_option('pylons_config_file')
#    fileConfig(config_file)
#    wsgi_app = loadapp('config:%s' % config_file, relative_to='.')

# add your model's MetaData object here
# for 'autogenerate' support
from sauce import model
target_metadata = model.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, version_table='migrate_version')

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table='migrate_version'
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
