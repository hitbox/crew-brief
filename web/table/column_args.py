from crew_brief.formatter import mdy_formatter

created_at_args = {
    'label': 'Created At',
    'formatter': mdy_formatter,
}

updated_at_args = {
    'label': 'Updated At',
    'formatter': mdy_formatter,
}

iata_code_args = {
    'attrs': {
        'class': 'data',
    },
}

icao_code_args = {
    'attrs': {
        'class': 'data',
    },
}

column_args = {
    'created_at': created_at_args,
    'updated_at': updated_at_args,
    'iata_code': iata_code_args,
    'icao_code': icao_code_args,
}
