"""create tickets table

Revision ID: 0001_init_tickets
Revises: 
Create Date: 2026-05-26 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init_tickets'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'ticket',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=255), nullable=True),
    )


def downgrade():
    op.drop_table('ticket')
