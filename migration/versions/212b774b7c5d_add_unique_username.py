"""Add unique username

Revision ID: 212b774b7c5d
Revises: 93d0945e9530
Create Date: 2025-07-24 14:59:09.122131

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '212b774b7c5d'
down_revision = '93d0945e9530'
branch_labels = None
depends_on = None

def upgrade():
    """Upgrade schema."""
    op.create_unique_constraint(None, 'user', ['username'])

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'user', type_='unique')
