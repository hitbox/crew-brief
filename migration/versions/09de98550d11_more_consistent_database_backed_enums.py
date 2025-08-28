"""More consistent database backed enums

Revision ID: 09de98550d11
Revises: 7498d8dc32b2
Create Date: 2025-08-27 13:21:20.785686

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '09de98550d11'
down_revision = '7498d8dc32b2'
branch_labels = None
depends_on = None

def upgrade():
    """
    Upgrade schema.
    """
    op.add_column('object_creator', sa.Column('description', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'object_creator', ['name'])
    op.add_column('scraper_step_type', sa.Column('description', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'scraper_step_type', ['name'])

def downgrade():
    """
    Downgrade schema.
    """
    op.drop_constraint(None, 'scraper_step_type', type_='unique')
    op.drop_column('scraper_step_type', 'description')
    op.drop_constraint(None, 'object_creator', type_='unique')
    op.drop_column('object_creator', 'description')
