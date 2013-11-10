"""LTI

Revision ID: 22b9ebe02912
Revises: 425be68ff414
Create Date: 2013-11-10 17:33:40.942971

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
revision = '22b9ebe02912'
down_revision = '425be68ff414'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():
    op.create_table('lti',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('oauth_key', sa.Unicode(length=255), nullable=True),
        sa.Column('oauth_secret', sa.Unicode(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lti_to',
        sa.Column('lti_id', sa.Integer(), nullable=False),
        sa.Column('assignment_id', sa.Integer(), nullable=True),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['assignment_id'], ['assignments.id'], ),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['lti_id'], ['lti.id'], ),
        sa.PrimaryKeyConstraint('lti_id')
    )


def downgrade():
    op.drop_table('lti_to')
    op.drop_table('lti')
