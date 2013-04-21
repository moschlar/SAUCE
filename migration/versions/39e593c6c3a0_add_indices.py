# -*- coding: utf-8 -*-
"""Add indices

Needed due to git commit 94e3bbc, between release versions 1.1 and 1.2

Revision ID: 39e593c6c3a0
Revises: 5894175a5dd9
Create Date: 2012-11-12 22:39:47.938656

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
revision = '39e593c6c3a0'
down_revision = '5894175a5dd9'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():

    #assignment.py

    op.create_index('ix_assignments_event_id', 'assignments', ['event_id'])
    op.create_index('ix_assignments_sheet_id', 'assignments', ['sheet_id'])

    op.create_index('idx_sheet_assignment', 'assignments', ['sheet_id', 'assignment_id'], unique=True)
    op.create_index('idx_event_assignment', 'assignments', ['event_id', 'assignment_id'], unique=True)

    op.create_index('ix_sheets_event_id', 'sheets', ['event_id'])
    op.create_index('idx_event_sheet', 'sheets', ['event_id', 'sheet_id'], unique=True)

    #event.py

    op.create_index('idx_event_lesson', 'lessons', ['event_id', 'lesson_id'], unique=True)

    #news.py

    #op.alter_column('newsitems', 'event_id', index=True)
    op.create_index('ix_newsitems_event_id', 'newsitems', ['event_id'])

    #submission.py

    op.create_index('ix_submissions_assignment_id', 'submissions', ['assignment_id'])
    op.create_index('ix_submissions_user_id', 'submissions', ['user_id'])

    op.create_index('ix_judgements_submission_id', 'judgements', ['submission_id'])

    #test.py

    op.create_index('ix_tests_assignment_id', 'tests', ['assignment_id'])

    op.create_index('ix_testruns_test_id', 'testruns', ['test_id'])
    op.create_index('ix_testruns_submission_id', 'testruns', ['submission_id'])

    op.create_index('idx_test_submission', 'testruns', ['test_id', 'submission_id'])

    #user.py

    op.create_index('ix_users_user_name', 'users', ['user_name'], unique=True)
    op.create_index('ix_users_email_address', 'users', ['email_address'], unique=True)

    op.create_index('ix_teams_lesson_id', 'teams', ['lesson_id'])


def downgrade():

    #assignment.py

    op.drop_index('ix_assignments_event_id', 'assignments')
    op.drop_index('ix_assignments_sheet_id', 'assignments')

    op.drop_index('idx_sheet_assignment', 'assignments')
    op.drop_index('idx_event_assignment', 'assignments')

    op.drop_index('ix_sheets_event_id', 'sheets')
    op.drop_index('idx_event_sheet', 'sheets')

    #event.py

    op.drop_index('idx_event_lesson', 'lessons')

    #news.py

    op.drop_index('ix_newsitems_event_id', 'newsitems')

    #submission.py

    op.drop_index('ix_submissions_assignment_id', 'submissions')
    op.drop_index('ix_submissions_user_id', 'submissions')

    op.drop_index('ix_judgements_submission_id', 'judgements')

    #test.py

    op.drop_index('ix_tests_assignment_id', 'tests')

    op.drop_index('ix_testruns_test_id', 'testruns')
    op.drop_index('ix_testruns_submission_id', 'testruns')

    op.drop_index('idx_test_submission', 'testruns')

    #user.py

    op.drop_index('ix_users_user_name', 'users')
    op.drop_index('ix_users_email_address', 'users')

    op.drop_index('ix_teams_lesson_id', 'teams')
