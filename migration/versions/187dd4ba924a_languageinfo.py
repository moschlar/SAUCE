# -*- coding: utf-8 -*-
"""languageinfo

Adds languageinfo cmd fields to Interpreter and Compiler

Revision ID: 187dd4ba924a
Revises: 39e593c6c3a0
Create Date: 2013-01-14 18:52:16.988269

"""
#
# # SAUCE - System for AUtomated Code Evaluation
# # Copyright (C) 2013 Moritz Schlarb
# #
# # This program is free software: you can redistribute it and/or modify
# # it under the terms of the GNU Affero General Public License as published by
# # the Free Software Foundation, either version 3 of the License, or
# # any later version.
# #
# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# # GNU Affero General Public License for more details.
# #
# # You should have received a copy of the GNU Affero General Public License
# # along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# revision identifiers, used by Alembic.
revision = '187dd4ba924a'
down_revision = '39e593c6c3a0'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():
    op.add_column('compilers', sa.Column('version_cmd', sa.Unicode(255), nullable=True, default=u'--version'))
    op.add_column('compilers', sa.Column('help_cmd', sa.Unicode(255), nullable=True, default=u'--help'))

    op.add_column('interpreters', sa.Column('version_cmd', sa.Unicode(255), nullable=True, default=u'--version'))
    op.add_column('interpreters', sa.Column('help_cmd', sa.Unicode(255), nullable=True, default=u'--help'))


def downgrade():
    op.drop_column('compilers', 'version_cmd')
    op.drop_column('compilers', 'help_cmd')

    op.drop_column('interpreters', 'version_cmd')
    op.drop_column('interpreters', 'help_cmd')
