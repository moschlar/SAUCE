"""Judgement.public

Revision ID: 1e52c8ddf5a0
Revises: 17da3b00f3f0
Create Date: 2014-10-26 14:45:41.812366

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
revision = '1e52c8ddf5a0'
down_revision = '17da3b00f3f0'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():
    op.add_column('judgements',
        sa.Column('public', sa.Boolean(), nullable=False,
            default=True, server_default='True'))


def downgrade():
    op.drop_column('judgements', 'public')
