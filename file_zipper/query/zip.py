import sqlalchemy as sa

from file_zipper.model import FileType
from file_zipper.model import Path

def file_type_from_mime_type(mime_type):
    """
    """
    return (
        sa.select(FileType.id)
        .filter(FileType.mime_type == mime_type)
        .scalar_subquery()
    )

def pdf_file_type():
    return file_type_from_mime_type('application/pdf')

def zip_file_type():
    return file_type_from_mime_type('application/x-zip-compressed')

def zip_paths_statement():
    """
    Statement that matches ZIP paths to PDF paths.
    """
    path_id_column = Path.id.label('path_id')
    zip_file = (
        sa.select(path_id_column)
        .filter(Path.file_type_id == zip_file_type())
        .cte('zip_file')
    )
    pdf_file = (
        sa.select(path_id_column)
        .filter(Path.file_type_id == pdf_file_type())
        .cte('pdf_file')
    )

    zip_path = sa.orm.aliased(Path)
    pdf_path = sa.orm.aliased(Path)

    zip_path_match = sa.orm.aliased(PathMatch)
    pdf_path_match = sa.orm.aliased(PathMatch)

    stmt = sa.select(
        zip_path,
        pdf_path,
    ).select_from(
        zip_file,
    ).join(
        zip_path,
        zip_file.c.path_id == zip_path.id,
    ).join(
        zip_path_match,
        zip_path_match.path_id == zip_path.id,
    ).join(
        pdf_path_match,
        pdf_path_match.path_id == pdf_path.id,
    ).join(
        pdf_file,
        sa.and_(
            pdf_path.id == pdf_file.c.path_id,

            zip_path_match.data['airline']
                == pdf_path_match.data['airline'],

            zip_path_match.data['origin_iata']
                == pdf_path_match.data['origin_iata'],

            zip_path_match.data['destination_iata']
                == pdf_path_match.data['destination_iata'],

            zip_path_match.data['flight_number']
                == pdf_path_match.data['flight_number'],
        ),
    )
    return stmt

def match_with_pdf_statement(zip_path_id):
    pdf_file = (
        sa.select(Path.id.label('path_id'))
        .filter(Path.file_type_id == pdf_file_type())
        .cte('pdf_file')
    )

    zip_path = sa.orm.aliased(Path)
    pdf_path = sa.orm.aliased(Path)

    zip_path_match = sa.orm.aliased(PathMatch)
    pdf_path_match = sa.orm.aliased(PathMatch)

    stmt = sa.select(
        zip_path,
        pdf_path,
    ).select_from(
        zip_path,
    ).join(
        zip_path_match,
        zip_path_match.path_id == zip_path.id,
    ).join(
        pdf_path_match,
        pdf_path_match.path_id == pdf_path.id,
    ).join(
        pdf_file,
        sa.and_(
            pdf_path.id == pdf_file.c.path_id,

            # Match data scraped from paths.
            # airline
            zip_path_match.data['airline'] == pdf_path_match.data['airline'],

            # origin_iata
            zip_path_match.data['origin_iata'] == pdf_path_match.data['origin_iata'],

            # destination_iata
            zip_path_match.data['destination_iata'] == pdf_path_match.data['destination_iata'],

            # flight_number
            zip_path_match.data['flight_number'] == pdf_path_match.data['flight_number'],

            #
            #zip_path_match.data['flight_date'] == pdf_path_match.data['datetime1'][:10],
        ),
    ).filter(
        zip_path.id == zip_path_id,
    )
    return stmt
