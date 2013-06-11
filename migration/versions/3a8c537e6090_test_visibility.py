"""test_visibility

Differentiate test visibility

Revision ID: 3a8c537e6090
Revises: 6bceed82300
Create Date: 2013-06-12 01:05:45.675323

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
revision = '3a8c537e6090'
down_revision = '6bceed82300'

from alembic import op, context
#from alembic.operations import Operations as op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
#TODO: This must be wrong - I need a reflected model here
from sauce.model import Test


def upgrade():
    cntxt = context.get_context()
    Session = sessionmaker(bind=cntxt.bind)

    op.add_column('tests', sa.Column('result_public', sa.Boolean(), nullable=True))
    op.add_column('tests', sa.Column('data_public', sa.Boolean(), nullable=True))

    session = Session()
    for test in session.query(Test):
        test.result_public = test.data_public = test.visible
    session.commit()

    op.alter_column('tests', 'result_public', nullable=False)
    op.alter_column('tests', 'data_public', nullable=False)


def downgrade():
    op.drop_column('tests', 'data_public')
    op.drop_column('tests', 'result_public')
