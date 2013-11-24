"""event_enroll

Revision ID: 425be68ff414
Revises: 3be6a175f769
Create Date: 2013-10-28 11:22:00.036581

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
revision = '425be68ff414'
down_revision = '3be6a175f769'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa

event_enroll = sa.Enum('event', 'lesson', 'lesson_team', 'team', 'team_new', name='event_enroll')


def upgrade():
    event_enroll.create(op.get_bind(), checkfirst=False)
    op.add_column('events', sa.Column('enroll', event_enroll, nullable=True))


def downgrade():
    event_enroll.drop(op.get_bind(), checkfirst=False)
    op.drop_column('events', 'enroll')
