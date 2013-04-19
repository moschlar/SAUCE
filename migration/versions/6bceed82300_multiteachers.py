"""Multiple teachers and tutors for events and lessons

Revision ID: 6bceed82300
Revises: 2fda8a9f7e6f
Create Date: 2013-04-19 22:28:51.095058

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
revision = '6bceed82300'
down_revision = '2fda8a9f7e6f'

from alembic import op, context
#from alembic.operations import Operations as op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sauce.model import Event, Lesson


def upgrade():
    cntxt = context.get_context()
    Session = sessionmaker(bind=cntxt.bind)

    op.create_table(u'event_teachers',
        sa.Column(u'user_id', sa.INTEGER(), nullable=False),
        sa.Column(u'event_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], [u'events.id'], ),
        sa.ForeignKeyConstraint(['user_id'], [u'users.id'], ),
        sa.PrimaryKeyConstraint(u'user_id', u'event_id')
    )
    session = Session()
    event_teachers = session.query(Event).all()
    for e in event_teachers:
        e.teachers = [e._teacher]
    session.commit()

    op.create_table(u'lesson_tutors',
        sa.Column(u'user_id', sa.INTEGER(), nullable=False),
        sa.Column(u'lesson_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['lesson_id'], [u'lessons.id'], ),
        sa.ForeignKeyConstraint(['user_id'], [u'users.id'], ),
        sa.PrimaryKeyConstraint(u'user_id', u'lesson_id')
    )
    session = Session()
    lesson_tutors = session.query(Lesson).all()
    for l in lesson_tutors:
        l.tutors = [l._tutor]
    session.commit()

    op.alter_column('lessons', u'tutor_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade():
    op.drop_table(u'event_teachers')
    op.drop_table(u'lesson_tutors')
    op.alter_column('lessons', u'tutor_id',
               existing_type=sa.Integer(),
               nullable=False)
