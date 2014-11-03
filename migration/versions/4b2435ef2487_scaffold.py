"""Source code scaffolds

Revision ID: 4b2435ef2487
Revises: 453b256dce6b
Create Date: 2014-03-16 22:05:22.960849

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
revision = '4b2435ef2487'
down_revision = '453b256dce6b'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():
    op.add_column('assignments', sa.Column('submission_scaffold_foot', sa.Unicode(10485760), nullable=True))
    op.add_column('assignments', sa.Column('submission_scaffold_head', sa.Unicode(10485760), nullable=True))
    op.add_column('assignments', sa.Column('submission_filename', sa.Unicode(255), nullable=True))
    op.add_column('assignments', sa.Column('submission_template', sa.Unicode(10485760), nullable=True))
    op.add_column('assignments', sa.Column('submission_scaffold_show', sa.Boolean(), nullable=False,
        default=True, server_default='True'))


def downgrade():
    op.drop_column('assignments', 'submission_scaffold_show')
    op.drop_column('assignments', 'submission_template')
    op.drop_column('assignments', 'submission_filename')
    op.drop_column('assignments', 'submission_scaffold_head')
    op.drop_column('assignments', 'submission_scaffold_foot')
