import copy

import openpyxl

from crew_brief import configlib
from crew_brief import constants
from crew_brief import databaselib
from crew_brief import discover
from crew_brief import nodes
from crew_brief import output
from crew_brief import rowifier
from crew_brief import schema
from crew_brief import shapers

def sample_output(args):
    """
    Produce a sample Excel output.
    """
    limit = args.number
    config = configlib.from_args(args)
    path_format = args.output.format
    autofit_with_excel = args.autofit_with_excel
    excel_converter = output.ExcelConverter()

    member_data_shaper = shapers.MemberDataShaper()

    database = databaselib.database_from_config(config)

    database = discover.get_interesting_files(database)
    if not database:
        raise ValueError('No interesting data found.')

    for count, original_zip_data in enumerate(database):
        if count == limit:
            break

        # Load/convert saved JSON data to types.
        typed_zip_data = schema.pickle_schema.load(original_zip_data)

        # Raise for member_data is None
        member_data = typed_zip_data['member_data']
        if member_data is None:
            raise ValueError('member_data is None.')

        # Copy and apply custom data shaping.
        shaped_member_data = copy.deepcopy(member_data)
        member_data_shaper(shaped_member_data)

        # Create workbook.
        excel_converter = output.ExcelConverter()
        wb = excel_converter(
            path_data = typed_zip_data['path_data'],
            user_events_data = shaped_member_data,
            original_user_events_data = member_data,
            flattened = args.flattened,
        )

        output_path = path_format(**typed_zip_data)
        wb.save(output_path)
