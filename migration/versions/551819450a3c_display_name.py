"""display_name

Add display_name field to User (again)

Revision ID: 551819450a3c
Revises: 187dd4ba924a
Create Date: 2013-04-08 21:43:51.436466

"""
#
#

# revision identifiers, used by Alembic.
revision = '551819450a3c'
down_revision = '187dd4ba924a'

from alembic import op
from alembic.operations import Operations as op
import sqlalchemy as sa



def upgrade():
    op.add_column('users', sa.Column('display_name', sa.Unicode(255), nullable=True, default=None))


def downgrade():
    op.drop_column('users', 'display_name')
