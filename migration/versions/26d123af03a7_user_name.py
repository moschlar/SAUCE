"""user_name

Revision ID: 26d123af03a7
Revises: 22b9ebe02912
Create Date: 2013-11-10 18:15:56.423575

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
revision = '26d123af03a7'
down_revision = '22b9ebe02912'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():
    op.alter_column('users', 'user_name', type_=sa.Unicode(255), existing_type=sa.Unicode(16))


def downgrade():
    op.alter_column('users', 'user_name', type_=sa.Unicode(16), existing_type=sa.Unicode(255))
