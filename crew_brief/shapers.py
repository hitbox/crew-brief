class EventDetailsShaper:
    """
    Expand dicts that have values as keys.
    """

    expand_key_as_value = set([
        'assignedLandingDuty',
        'assignedTakeOffDuty',
        'withdrawnLandingDuty',
        'withdrawnTakeOffDuty',
    ])

    def expand_item(self, data):
        assert isinstance(data, dict)
        assert len(data) == 1
        key_value = next(iter(data.items()))
        return dict(zip(['rank', 'name'], key_value))

    def __call__(self, event_details):
        for key, val in event_details.items():
            if key in self.expand_key_as_value:
                # val is a dict, expand its keys that should have been values.
                event_details[key] = self.expand_item(val)


class UserEventShaper:

    default_event_details_shaper_class = EventDetailsShaper

    def __init__(self, event_details_shaper=None):
        if event_details_shaper is None:
            event_details_shaper = self.default_event_details_shaper_class()
        self.event_details_shaper = event_details_shaper

    def __call__(self, user_event):
        if 'eventDetails' in user_event:
            self.event_details_shaper(user_event['eventDetails'])


class MemberDataShaper:
    """
    Callable applies shaper to userEvents.
    """

    default_user_event_shaper_class = UserEventShaper

    def __init__(self, user_event_shaper=None):
        if user_event_shaper is None:
            user_event_shaper = self.default_user_event_shaper_class()
        self.user_event_shaper = user_event_shaper

    def __call__(self, member_data):
        for user_event in member_data.get('userEvents', []):
            self.user_event_shaper(user_event)
