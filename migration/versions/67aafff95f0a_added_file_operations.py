"""Added file operations

Revision ID: 67aafff95f0a
Revises:
Create Date: 2025-07-22 11:46:30.983308

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision= '67aafff95f0a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """
    Upgrade schema.
    """
    # Add file operation tables.
    op.create_table('file_operation_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("description <> ''"),
        sa.CheckConstraint("name <> ''"),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file_operation_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("description <> ''"),
        sa.CheckConstraint("name <> ''"),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file_operation_status_transition',
        sa.Column('from_status_id', sa.Integer(), nullable=False),
        sa.Column('to_status_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['from_status_id'], ['file_operation_status.id'], ),
        sa.ForeignKeyConstraint(['to_status_id'], ['file_operation_status.id'], ),
        sa.PrimaryKeyConstraint('from_status_id', 'to_status_id')
    )
    op.create_table('file_operation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('leg_file_id', sa.Integer(), nullable=False),
        sa.Column('operation_type_id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.Column('target_file_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['leg_file_id'], ['leg_file.id'], ),
        sa.ForeignKeyConstraint(['operation_type_id'], ['file_operation_type.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['file_operation_status.id'], ),
        sa.ForeignKeyConstraint(['target_file_id'], ['leg_file.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    # Add some missing foreign keys.
    op.create_foreign_key(None, 'leg_file', 'mime_type', ['mime_type_id'], ['id'])
    op.alter_column('mime_type', 'is_mime_zip',
               existing_type=sa.BOOLEAN(),
               nullable=False)

def downgrade():
    """
    Downgrade schema.
    """
    op.alter_column('mime_type', 'is_mime_zip',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_table('file_operation')
    op.drop_table('file_operation_status_transition')
    op.drop_table('file_operation_type')
    op.drop_table('file_operation_status')
