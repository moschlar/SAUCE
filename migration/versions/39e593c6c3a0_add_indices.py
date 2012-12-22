"""Add indices

Needed due to git commit 94e3bbc, between release versions 1.1 and 1.2

Revision ID: 39e593c6c3a0
Revises: 5894175a5dd9
Create Date: 2012-11-12 22:39:47.938656

"""

# revision identifiers, used by Alembic.
revision = '39e593c6c3a0'
down_revision = '5894175a5dd9'

from alembic import op
#from alembic.operations import Operations as op
import sqlalchemy as sa


def upgrade():

    #assignment.py

    op.alter_column('assignments', 'event_id', index=True)
    op.alter_column('assignments', 'sheet_id', index=True)
    op.create_index('idx_sheet_assignment', 'assignments', ['sheet_id', 'assignment_id'], unique=True)
    op.create_index('idx_event_assignment', 'assignments', ['event_id', 'assignment_id'], unique=True)

    op.alter_column('sheets', 'event_id', index=True)
    op.create_index('idx_event_sheet', 'sheets', ['event_id', 'sheet_id'], unique=True)

    #event.py

    op.create_index('idx_event_lesson', 'lessons', ['event_id', 'lesson_id'], unique=True)

    #news.py

    op.alter_column('newsitems', 'event_id', index=True)

    #submission.py

    op.alter_column('submissions', 'assignment_id', index=True)
    op.alter_column('submissions', 'user_id', index=True)

    op.alter_column('judgement', 'submission_id', index=True)

    #test.py

    op.alter_column('tests', 'assignment_id', index=True)

    op.alter_column('testruns', 'test_id', index=True)
    op.alter_column('testruns', 'submission_id', index=True)

    op.create_index('idx_test_submission', 'testruns', ['test_id', 'submission_id'])

    #user.py

    op.alter_column('users', 'user_name', index=True)
    op.alter_column('users', 'email_address', index=True)

    op.alter_column('teams', 'lesson_id', index=True)


def downgrade():

    #assignment.py

    op.alter_column('assignments', 'event_id', index=False)
    op.alter_column('assignments', 'sheet_id', index=False)
    op.drop_index('idx_sheet_assignment', 'assignments', ['sheet_id', 'assignment_id'], unique=True)
    op.drop_index('idx_event_assignment', 'assignments', ['event_id', 'assignment_id'], unique=True)

    op.alter_column('sheets', 'event_id', index=False)
    op.drop_index('idx_event_sheet', 'sheets', ['event_id', 'sheet_id'], unique=True)

    #event.py

    op.drop_index('idx_event_lesson', 'lessons', ['event_id', 'lesson_id'], unique=True)

    #news.py

    op.alter_column('newsitems', 'event_id', index=False)

    #submission.py

    op.alter_column('submissions', 'assignment_id', index=False)
    op.alter_column('submissions', 'user_id', index=False)

    op.alter_column('judgement', 'submission_id', index=False)

    #test.py

    op.alter_column('tests', 'assignment_id', index=False)

    op.alter_column('testruns', 'test_id', index=False)
    op.alter_column('testruns', 'submission_id', index=False)

    op.drop_index('idx_test_submission', 'testruns', ['test_id', 'submission_id'])

    #user.py

    op.alter_column('users', 'user_name', index=False)
    op.alter_column('users', 'email_address', index=False)

    op.alter_column('teams', 'lesson_id', index=False)
