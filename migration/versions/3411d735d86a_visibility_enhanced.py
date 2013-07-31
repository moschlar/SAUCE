"""visibility_enhanced

Enhance visibility attributes

TODO: Value migration!

Revision ID: 3411d735d86a
Revises: 3a8c537e6090
Create Date: 2013-07-31 22:57:04.854223

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
revision = '3411d735d86a'
down_revision = '3a8c537e6090'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa



def upgrade():
    op.add_column('assignments', sa.Column('visibility', sa.Enum(u'anonymous', u'users', u'students', u'tutors', u'teachers', name='visibility_type'), nullable=False))
    op.alter_column('assignments', u'public',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.add_column('events', sa.Column('visibility', sa.Enum(u'anonymous', u'users', u'students', u'tutors', u'teachers', name='visibility_type'), nullable=False))
    op.alter_column('events', u'public',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.add_column('sheets', sa.Column('visibility', sa.Enum(u'anonymous', u'users', u'students', u'tutors', u'teachers', name='visibility_type'), nullable=False))
    op.alter_column('sheets', u'public',
               existing_type=sa.BOOLEAN(),
               nullable=True)


def downgrade():
    op.alter_column('sheets', u'public',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_column('sheets', 'visibility')
    op.alter_column('events', u'public',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_column('events', 'visibility')
    op.alter_column('assignments', u'public',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.drop_column('assignments', 'visibility')
