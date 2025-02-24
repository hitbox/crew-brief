from .constants import NESTED_KEY_SEP

class EventDetailsKey:
    """
    Callable ordering for eventDetails' keys. Mostly for sorting important keys
    to the front.
    """

    # Ordering list.
    # Empty lines to indicate keys that usually only appear together.
    # Consider eventDetails ordering by eventType.
    detail_keys = [

        # Many different eventType values.
        'waypoint',

        # eventType == DirectTo
        'fromWaypoint',
        'toWaypoint',
    ]

    event_type_ordering = dict(
        ReceivedAcceptedBP = [
            'receivedFromDevice',
            'categoriesReceived',
            'latestBpSequenceNumber',
            'latestBpVersion',
            'oldBpSequenceNumber',
            'oldBpVersion',
        ],
        SharedBP = [
            'sharedWithDevice',
            'categoriesShared',
        ],
        DutyAssignment = [
            NESTED_KEY_SEP.join(['assignedTakeOffDuty', 'name']),
            NESTED_KEY_SEP.join(['assignedTakeOffDuty', 'rank']),

            NESTED_KEY_SEP.join(['assignedLandingDuty', 'name']),
            NESTED_KEY_SEP.join(['assignedLandingDuty', 'rank']),

            NESTED_KEY_SEP.join(['withdrawnTakeOffDuty', 'name']),
            NESTED_KEY_SEP.join(['withdrawnTakeOffDuty', 'rank']),
        ],
    )

    def __call__(self, key, event_type):
        """
        If key is present in our ordering list return the index. Otherwise
        return the length of the list so as to sort the rest with the same
        precedence.
        """
        # Sorting is off. The subheader is somehow coming out different than
        # the values.
        # Also this one need to offset the event_type_ordering by the len(detail_keys)

        # Try to find an ordering list by eventType and then detail_keys.
        ordering_list = None
        if event_type in self.event_type_ordering:
            ordering_list = self.event_type_ordering[event_type]
        elif key in self.detail_keys:
            ordering_list = self.detail_keys

        # Use the ordering list or make the sort key all the same priority but
        # after any detail_keys.
        if ordering_list and key in ordering_list:
            return ordering_list.index(key)
        else:
            return len(self.detail_keys)
