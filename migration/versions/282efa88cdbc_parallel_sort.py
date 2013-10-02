"""Adds parallel_sort to 'tests'

Revision ID: 282efa88cdbc
Revises: 78d219a45996
Create Date: 2013-08-21 21:05:45.675323

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
revision = '282efa88cdbc'
down_revision = '3a8c537e6090'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():
    op.add_column('tests', sa.Column('parallel_sort', sa.BOOLEAN(), nullable=False, default=False, server_default='False'))


def downgrade():
    op.drop_column('tests', 'parallel_sort')
