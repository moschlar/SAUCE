"""testlabel

Add name field to Test

Revision ID: 6608530ab9e
Revises: 187dd4ba924a
Create Date: 2013-01-17 15:30:18.092589

"""

# revision identifiers, used by Alembic.
revision = '6608530ab9e'
down_revision = '187dd4ba924a'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():
    op.add_column('tests', sa.Column('name', sa.Unicode(255), nullable=True, default=None))


def downgrade():
    op.drop_column('tests', 'name')
