import os

NAME = 'crew_brief'

ENVIRON_CONFIG_KEY = f'{NAME.upper()}_CONFIG'

ZDATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

USER_EVENTS_KEY = 'userEvents'
EVENT_DETAILS_KEY = 'eventDetails'

LEG_IDENTIFIER_PARTS = [
    'company_code',
    'flight_number',
    'date',
    'origin',
    'destination',
    'letter_code',
]

LEG_IDENTIFIER_LABELS = {
    'company_code': 'Company Code',
    'flight_number': 'Flight Number',
    'date': 'Date',
    'origin': 'Origin',
    'destination': 'Destination',
    'letter_code': 'Letter Code',
}
