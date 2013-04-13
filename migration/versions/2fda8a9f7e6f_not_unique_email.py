"""Unrequire email_address to be unique

Revision ID: 2fda8a9f7e6f
Revises: 551819450a3c
Create Date: 2013-04-13 10:36:13.152181

"""

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
