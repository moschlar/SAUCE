"""test_failsafe_parsing

Revision ID: 453b256dce6b
Revises: 3a8c537e6090
Create Date: 2013-06-30 20:58:50.998667

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
revision = '453b256dce6b'
down_revision = '3a8c537e6090'

from alembic import op, context
#from alembic.operations import Operations as op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
#TODO: This must be wrong - I need a reflected model here
from sauce.model import Test


def upgrade():
    cntxt = context.get_context()
    Session = sessionmaker(bind=cntxt.bind)

    op.add_column('tests', sa.Column(u'failsafe_parsing', sa.Boolean(), nullable=True, default=False))

    session = Session()
    for test in session.query(Test):
        test.failsafe_parsing = False
    session.commit()

    op.alter_column('tests', 'result_public', nullable=False, default=False)


def downgrade():
    op.drop_column('tests', u'failsafe_parsing')
