"""Revise for history and file operations

Revision ID: d5e377e548cf
Revises: 212b774b7c5d
Create Date: 2025-07-28 16:14:51.424493

"""
import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd5e377e548cf'
down_revision = '212b774b7c5d'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """
    Upgrade schema.
    """
    op.create_table('change_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('user_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.CheckConstraint("name <> ''"),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file_operation_association',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_operation_id', sa.Integer(), nullable=False),
        sa.Column('leg_file_id', sa.Integer(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['file_operation_id'], ['file_operation.id'], ),
        sa.ForeignKeyConstraint(['leg_file_id'], ['leg_file.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('file_operation_history', sa.Column('change_type_id', sa.Integer(), nullable=False))
    op.add_column('file_operation_history', sa.Column('change_timestamp', sa.DateTime(timezone=True), nullable=False))
    op.add_column('file_operation_history', sa.Column('operation_user', sa.String(length=50), nullable=True))
    op.add_column('file_operation_history', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('file_operation_history', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.alter_column('file_operation_history', 'file_operation_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=False)
    op.drop_constraint(op.f('file_operation_history_operation_type_id_fkey'), 'file_operation_history', type_='foreignkey')
    op.drop_constraint(op.f('file_operation_history_target_file_id_fkey'), 'file_operation_history', type_='foreignkey')
    op.drop_constraint(op.f('file_operation_history_leg_file_id_fkey'), 'file_operation_history', type_='foreignkey')
    op.drop_constraint(op.f('file_operation_history_file_operation_id_fkey'), 'file_operation_history', type_='foreignkey')
    op.drop_constraint(op.f('file_operation_history_status_id_fkey'), 'file_operation_history', type_='foreignkey')
    op.drop_constraint(op.f('file_operation_history_change_status_id_fkey'), 'file_operation_history', type_='foreignkey')
    op.drop_constraint(op.f('file_operation_history_changed_by_id_fkey'), 'file_operation_history', type_='foreignkey')
    op.create_foreign_key(None, 'file_operation_history', 'file_operation', ['file_operation_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'file_operation_history', 'change_type', ['change_type_id'], ['id'])
    op.drop_column('file_operation_history', 'changed_by_id')
    op.drop_column('file_operation_history', 'change_status_id')
    op.drop_column('file_operation_history', 'changed_at')
    op.add_column('user', sa.Column('user_type_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'user', 'user_type', ['user_type_id'], ['id'])

def downgrade() -> None:
    """
    Downgrade schema.
    """
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'user_type_id')
    op.add_column('file_operation_history', sa.Column('changed_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.add_column('file_operation_history', sa.Column('change_status_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('file_operation_history', sa.Column('changed_by_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'file_operation_history', type_='foreignkey')
    op.drop_constraint(None, 'file_operation_history', type_='foreignkey')
    op.create_foreign_key(op.f('file_operation_history_changed_by_id_fkey'), 'file_operation_history', 'user', ['changed_by_id'], ['id'])
    op.create_foreign_key(op.f('file_operation_history_change_status_id_fkey'), 'file_operation_history', 'change_status', ['change_status_id'], ['id'])
    op.create_foreign_key(op.f('file_operation_history_status_id_fkey'), 'file_operation_history', 'file_operation_status', ['status_id'], ['id'])
    op.create_foreign_key(op.f('file_operation_history_file_operation_id_fkey'), 'file_operation_history', 'file_operation', ['file_operation_id'], ['id'])
    op.create_foreign_key(op.f('file_operation_history_leg_file_id_fkey'), 'file_operation_history', 'leg_file', ['leg_file_id'], ['id'])
    op.create_foreign_key(op.f('file_operation_history_target_file_id_fkey'), 'file_operation_history', 'leg_file', ['target_file_id'], ['id'])
    op.create_foreign_key(op.f('file_operation_history_operation_type_id_fkey'), 'file_operation_history', 'file_operation_type', ['operation_type_id'], ['id'])
    op.alter_column('file_operation_history', 'file_operation_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=False)
    op.drop_column('file_operation_history', 'updated_at')
    op.drop_column('file_operation_history', 'created_at')
    op.drop_column('file_operation_history', 'operation_user')
    op.drop_column('file_operation_history', 'change_timestamp')
    op.drop_column('file_operation_history', 'change_type_id')
    op.drop_table('file_operation_association')
    op.drop_table('user_type')
    op.drop_table('change_type')
