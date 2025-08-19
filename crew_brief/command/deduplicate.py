from collections import defaultdict

import sqlalchemy as sa

from crew_brief import configlib
from crew_brief.query import get_leg_identifier_unique_key_attrs
from crew_brief.query import select_duplicate_leg_identifiers

def add_parser(subparsers):
    parser = subparsers.add_parser('deduplicate')
    deduplicate_subparsers = parser.add_subparsers()
    add_deduplicate_leg_identifiers_parser(deduplicate_subparsers)

def add_deduplicate_leg_identifiers_parser(subparsers):
    """
    deduplicate_leg_identifiers
    """
    leg_identifier_parser = subparsers.add_parser(
        'leg_identifier',
        help = deduplicate_leg_identifiers.__doc__,
        description = deduplicate_leg_identifiers.__doc__,
    )
    leg_identifier_parser.add_argument('--commit', action='store_true', help='Commit changes.')
    configlib.add_config_option(leg_identifier_parser)
    leg_identifier_parser.set_defaults(func=deduplicate_leg_identifiers)

def deduplicate_leg_identifiers(args):
    """
    Deduplicate LegIdentifier objects and update referencing LegFile objects.
    """
    config = configlib.resolve_config(args.config)
    database_uri = getattr(config, 'DATABASE_URI')
    engine = sa.create_engine(database_uri)
    with sa.orm.Session(engine) as session:
        dupe_leg_identifiers_query = select_duplicate_leg_identifiers()

        dupe_leg_identifiers = defaultdict(set)
        unique_leg_identifiers = {}
        dupe_count = 0
        for leg_identifier in session.scalars(dupe_leg_identifiers_query):
            key = get_leg_identifier_unique_key_attrs(leg_identifier)
            if key not in unique_leg_identifiers:
                unique_leg_identifiers[key] = leg_identifier
            else:
                dupe_leg_identifiers[key].add(leg_identifier)
            dupe_count += 1

        updated_leg_files = 0
        for key, dupes in dupe_leg_identifiers.items():
            unique_id = unique_leg_identifiers[key].id
            for leg_identifier in dupes:
                leg_identifier.leg_file.leg_identifier_id = unique_id
                updated_leg_files += 1

        for dupes in dupe_leg_identifiers.values():
            for dupe in dupes:
                session.delete(dupe)

        print(f'{dupe_count=} {updated_leg_files=}')
        if args.commit:
            session.commit()
