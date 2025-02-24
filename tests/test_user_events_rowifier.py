import datetime
import unittest

from pprint import pprint

from crew_brief.constants import LEG_IDENTIFIER_LABELS
from crew_brief.rowifier import UserEventsRowifier
from crew_brief.schema import make_leg_identifier

TEST_DATA = dict(
    no_user_events = dict(
        input_data = dict(
            legIdentifier = dict(
                company_code = 'CCC',
                flight_number = '1234',
                date = datetime.date(2025, 1, 1),
                origin = 'ABC',
                destination = 'XYZ',
                letter_code = 'A',
            ),
            userId = '1234',
        ),
        expected_rows = (
            # (Styling Hint, values for row)
            ('header', ('eventTimeStamp', 'status', 'eventType', 'eventDetails')),
            ('empty', ()),
            ('header', ('legIdentifier',)),
            ('legIdentifier header', tuple(LEG_IDENTIFIER_LABELS.values())),
            ('legIdentifier values', ('CCC', '1234', '2025-01-01', 'ABC', 'XYZ', 'A')),
            ('empty', ()),
            ('userId field_and_value', ('userId', '1234')),
        ),
    ),

    has_user_events_no_event_details  = dict(
        input_data = dict(
            legIdentifier = dict(
                company_code = 'CCC',
                flight_number = '1234',
                date = datetime.date(2025, 1, 1),
                origin = 'ABC',
                destination = 'XYZ',
                letter_code = 'A',
            ),
            userId = '1234',
            userEvents = [
                dict(
                    eventTimeStamp = datetime.datetime(2025, 1, 2, 3, 4, 5, 6),
                    eventType = 'TypeOfEvent',
                    status = 'SuccessStatus',
                    eventDetails = {},
                ),
            ],
        ),
        expected_rows = (
            ('header',
                ('eventTimeStamp', 'status', 'eventType', 'eventDetails')),
            ('user_event_fields_and_values',
                ('2025-01-02 03:04:05.000006', 'SuccessStatus',
                 'TypeOfEvent')),
            ('empty', ()),
            ('header', ('legIdentifier',)),
            ('legIdentifier header',
                ('Company Code',
                 'Flight Number',
                 'Date',
                 'Origin',
                 'Destination',
                 'Letter Code')),
            ('legIdentifier values',
                ('CCC', '1234', '2025-01-01', 'ABC', 'XYZ', 'A')),
            ('empty', ()),
            ('userId field_and_value', ('userId', '1234')),
        ),
    ),

    event_detail_simple_datetime  = dict(
        input_data = dict(
            legIdentifier = dict(
                company_code = 'CCC',
                flight_number = '1234',
                date = datetime.date(2025, 1, 1),
                origin = 'ABC',
                destination = 'XYZ',
                letter_code = 'A',
            ),
            userId = '1234',
            userEvents = [
                dict(
                    eventTimeStamp = datetime.datetime(2025, 1, 2, 3, 4, 5, 6),
                    eventType = 'TypeOfEvent',
                    status = 'SuccessStatus',
                    eventDetails = dict(
                        dt_field = datetime.datetime(2025, 1, 2, 3, 4, 5, 6),
                    ),
                ),
            ],
        ),
        expected_rows = (
            ('header',
                ('eventTimeStamp', 'status', 'eventType', 'eventDetails')),
            ('user_event_fields_and_values',
                ('2025-01-02 03:04:05.000006', 'SuccessStatus',
                 'TypeOfEvent', 'dt_field')),
            ('empty', ('2025-01-02 03:04:05.000006', )),
            ('header', ('legIdentifier',)),
            ('legIdentifier header',
                ('Company Code',
                 'Flight Number',
                 'Date',
                 'Origin',
                 'Destination',
                 'Letter Code')),
            ('legIdentifier values',
                ('CCC', '1234', '2025-01-01', 'ABC', 'XYZ', 'A')),
            ('empty', ()),
            ('userId field_and_value', ('userId', '1234')),
        ),
    ),

)

@unittest.skip('Skipping test for UserEventRow.')
class TestUserEventsRowifier(unittest.TestCase):

    def check_data(self, expected_rows, output_rows):
        items = zip(
            expected_rows,
            output_rows,
            strict = True,
        )
        for expected, output in items:
            self.assertEqual(expected, output.row)

    def check_test(self, name):
        input_data = TEST_DATA[name]['input_data']
        expected_rows = TEST_DATA[name]['expected_rows']
        user_events_rowifier = UserEventsRowifier()
        output_rows = user_events_rowifier(input_data, input_data)
        self.check_data(expected_rows, output_rows)

    def test_user_events_rowifier(self):
        self.check_test('no_user_events')

    def print_output(self, name):
        # Method for debugging/figuring out what I want to have come out of
        # rowifier.
        input_data = TEST_DATA[name]['input_data']
        user_events_rowifier = UserEventsRowifier()
        output = tuple(user_events_rowifier(input_data))
        pprint(output)

    def test_has_user_events_no_event_details(self):
        self.check_test('has_user_events_no_event_details')

    def __disable_test_event_detail_simple_datetime(self):
        self.print_output('event_detail_simple_datetime')
