"""Add shadow history

Revision ID: 93d0945e9530
Revises: 055da66208bf
Create Date: 2025-07-24 14:51:56.726255

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '93d0945e9530'
down_revision = '055da66208bf'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """
    Upgrade schema.
    """
    op.create_table('change_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('realname', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("realname <> ''"),
        sa.CheckConstraint("username <> ''"),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file_operation_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_operation_id', sa.Integer(), nullable=False),
        sa.Column('change_status_id', sa.Integer(), nullable=False),
        sa.Column('changed_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('changed_by_id', sa.Integer(), nullable=False),
        sa.Column('leg_file_id', sa.Integer(), nullable=False),
        sa.Column('operation_type_id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.Column('enabled_at', sa.DateTime(), nullable=True),
        sa.Column('target_file_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['change_status_id'], ['change_status.id'], ),
        sa.ForeignKeyConstraint(['changed_by_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['file_operation_id'], ['file_operation.id'], ),
        sa.ForeignKeyConstraint(['leg_file_id'], ['leg_file.id'], ),
        sa.ForeignKeyConstraint(['operation_type_id'], ['file_operation_type.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['file_operation_status.id'], ),
        sa.ForeignKeyConstraint(['target_file_id'], ['leg_file.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    """
    Downgrade schema.
    """
    op.drop_table('file_operation_history')
    op.drop_table('user')
    op.drop_table('change_status')
