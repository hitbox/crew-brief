"""
Common constant values.
"""

NAME = 'crew_brief'

ENVIRON_CONFIG_KEY = f'{NAME.upper()}_CONFIG'

ZDATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

# legIdentifier parts as they appear in the original string.
LEG_IDENTIFIER_PARTS = [
    'company_code',
    'flight_number',
    'date',
    'origin',
    'destination',
    'letter_code',
]

# Labels and ordering for rowifying.
LEG_IDENTIFIER_LABELS = {
    'date': 'Date',
    'flight_number': 'Flight Number',
    'origin': 'Origin',
    'destination': 'Destination',
    'company_code': 'Company Code',
    'letter_code': 'Letter Code',
}

# Format of date in legIdentifier string.
LEG_IDENTIFIER_DATE_FORMAT = '%d%b%Y'

# Separator for nested keys from unfolding.
NESTED_KEY_SEP = '\n'
