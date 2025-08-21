"""
PathFlavor elevated to database object. Scraper and scraper steps objects.

Revision ID: 7498d8dc32b2
Revises: d5e377e548cf
Create Date: 2025-08-20 16:16:32.297105

"""
import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7498d8dc32b2'
down_revision = 'd5e377e548cf'
branch_labels = None
depends_on = None

# Rows for enum PathFlavorEnum.
path_flavor_rows = [
    {'id': 1, 'name': 'auto'},
    {'id': 2, 'name': 'posix'},
    {'id': 3, 'name': 'nt'},
]

def upgrade():
    """
    Upgrade schema.
    """
    op.create_table('exception_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.CheckConstraint("name <> ''"),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('object_creator',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.CheckConstraint("name <> ''"),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('scraper_step_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exception_instance',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('exception_type_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('traceback', sa.String(), nullable=False),
        sa.CheckConstraint("message <> ''"),
        sa.CheckConstraint("traceback <> ''"),
        sa.ForeignKeyConstraint(['exception_type_id'], ['exception_type.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scraper_step',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scraper_id', sa.Integer(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['scraper_id'], ['scraper.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['scraper_step_type.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scraper_step_function',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('function_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['scraper_step.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scraper_step_object',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['object_creator.id'], ),
    sa.ForeignKeyConstraint(['id'], ['scraper_step.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scraper_step_regex',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('regex_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['scraper_step.id'], ),
    sa.ForeignKeyConstraint(['regex_id'], ['regex.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scraper_step_schema',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('schema_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['scraper_step.id'], ),
    sa.ForeignKeyConstraint(['schema_id'], ['schema.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('leg_file_scraper_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('leg_file_id', sa.Integer(), nullable=False),
    sa.Column('scraper_step_id', sa.Integer(), nullable=False),
    sa.Column('exception_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['exception_id'], ['exception_instance.id'], ),
    sa.ForeignKeyConstraint(['leg_file_id'], ['leg_file.id'], ),
    sa.ForeignKeyConstraint(['scraper_step_id'], ['scraper_step.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('leg_identifier', 'ofp_version')

    # Create path_flavor table and populate. Needed for next table.
    path_flavor_table = op.create_table('path_flavor',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.CheckConstraint("name <> ''"),
        sa.PrimaryKeyConstraint('id'),
    )
    op.bulk_insert(path_flavor_table, path_flavor_rows)

    # Add nullable first, update, and then alter not-nullable.
    op.add_column(
        'os_walk',
        sa.Column('path_flavor_id', sa.Integer(), nullable=True),
    )
    # Update new column from list of dicts above.
    os_walk_table = sa.table(
        'os_walk',
        sa.Column('path_flavor', sa.String()), # old enum field.
        sa.Column('path_flavor_id', sa.Integer()),
    )
    for path_flavor_row in path_flavor_rows:
        op.execute(
            os_walk_table.update()
            .where(
                sa.cast(os_walk_table.c.path_flavor, sa.String) == path_flavor_row['name']
            )
            .values({'path_flavor_id': path_flavor_row['id']})
        )
    op.alter_column('os_walk', 'path_flavor_id', nullable=False)

    op.create_foreign_key(None, 'os_walk', 'path_flavor', ['path_flavor_id'], ['id'])

    op.drop_column('os_walk', 'path_flavor')

def downgrade():
    """
    Downgrade schema.
    """
    op.add_column('os_walk', sa.Column('path_flavor', postgresql.ENUM('auto', 'posix', 'nt', name='path_flavor_enum'), server_default=sa.text("'auto'::path_flavor_enum"), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'os_walk', type_='foreignkey')
    op.drop_column('os_walk', 'path_flavor_id')
    op.add_column('leg_identifier', sa.Column('ofp_version', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_table('leg_file_scraper_history')
    op.drop_table('scraper_step_schema')
    op.drop_table('scraper_step_regex')
    op.drop_table('scraper_step_object')
    op.drop_table('scraper_step_function')
    op.drop_table('scraper_step')
    op.drop_table('exception_instance')
    op.drop_table('scraper_step_type')
    op.drop_table('path_flavor')
    op.drop_table('object_creator')
    op.drop_table('exception_type')
