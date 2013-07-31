"""Unrequire email_address to be unique

Revision ID: 2fda8a9f7e6f
Revises: 551819450a3c
Create Date: 2013-04-13 10:36:13.152181

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
revision = '2fda8a9f7e6f'
down_revision = '551819450a3c'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():
    op.alter_column('users', 'email_address', nullable=False)


def downgrade():
    op.alter_column('users', 'email_address', nullable=True)
