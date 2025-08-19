"""Add enabled_at

Revision ID: 055da66208bf
Revises: 633b2653af91
Create Date: 2025-07-22 16:50:15.098454

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '055da66208bf'
down_revision = '633b2653af91'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('file_operation', sa.Column('enabled_at', sa.DateTime(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('file_operation', 'enabled_at')
