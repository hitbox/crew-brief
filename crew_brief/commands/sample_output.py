from crew_brief import configlib
from crew_brief import databaselib
from crew_brief import discover
from crew_brief import schema
from crew_brief import workbook

def sample_output(args):
    """
    Produce a sample Excel output.
    """
    limit = args.number
    config = configlib.from_args(args)
    path_format = args.output.format
    autofit_with_excel = args.autofit_with_excel

    database = databaselib.database_from_config(config)

    database = discover.get_interesting_files(database)
    if not database:
        raise ValueError('No interesting data found.')

    for count, zip_data in enumerate(database):
        if count == limit:
            break

        # Load/convert saved JSON data to types.
        typed_zip_data = schema.pickle_schema.load(zip_data)

        wb = workbook.build_workbook(zip_data, typed_zip_data)

        output_path = path_format(**typed_zip_data)
        wb.save(output_path)
