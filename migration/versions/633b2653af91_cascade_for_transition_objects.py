"""Cascade for transition objects

Revision ID: 633b2653af91
Revises: eff1e7ad3bd0
Create Date: 2025-07-22 16:34:01.425252

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '633b2653af91'
down_revision = 'eff1e7ad3bd0'
branch_labels = None
depends_on = None

def upgrade():
    """Upgrade schema."""
    # Update foreign keys with cascade on delete.
    op.drop_constraint(op.f('file_operation_status_transition_to_status_id_fkey'), 'file_operation_status_transition', type_='foreignkey')
    op.drop_constraint(op.f('file_operation_status_transition_from_status_id_fkey'), 'file_operation_status_transition', type_='foreignkey')
    op.create_foreign_key(None, 'file_operation_status_transition', 'file_operation_status', ['to_status_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'file_operation_status_transition', 'file_operation_status', ['from_status_id'], ['id'], ondelete='CASCADE')

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'file_operation_status_transition', type_='foreignkey')
    op.drop_constraint(None, 'file_operation_status_transition', type_='foreignkey')
    op.create_foreign_key(op.f('file_operation_status_transition_from_status_id_fkey'), 'file_operation_status_transition', 'file_operation_status', ['from_status_id'], ['id'])
    op.create_foreign_key(op.f('file_operation_status_transition_to_status_id_fkey'), 'file_operation_status_transition', 'file_operation_status', ['to_status_id'], ['id'])
