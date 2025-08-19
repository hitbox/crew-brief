"""Adjusting file operations objects

Revision ID: eff1e7ad3bd0
Revises: 67aafff95f0a
Create Date: 2025-07-22 16:28:43.324053

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'eff1e7ad3bd0'
down_revision = '67aafff95f0a'
branch_labels = None
depends_on = None

def upgrade():
    """Upgrade schema."""
    op.create_unique_constraint(None, 'file_operation_status', ['name'])
    op.create_foreign_key(None, 'leg_identifier', 'ofp_version', ['ofp_version_id'], ['id'])

def downgrade():
    """Downgrade schema."""
    op.drop_constraint(None, 'leg_identifier', type_='foreignkey')
    op.drop_constraint(None, 'file_operation_status', type_='unique')
