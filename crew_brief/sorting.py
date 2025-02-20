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

        # eventType == ReceivedAcceptedBP
        'receivedFromDevice',
        'categoriesReceived',
        'latestBpSequenceNumber',
        'latestBpVersion',
        'oldBpSequenceNumber',
        'oldBpVersion',
    ]

    def __call__(self, key):
        """
        If key is present in our ordering list return the index. Otherwise
        return the length of the list so as to sort the rest with the same
        precedence.
        """
        if key in self.detail_keys:
            # Priority from list.
            return self.detail_keys.index(key)
        else:
            # Otherwise, same priority but after important keys.
            return len(self.detail_keys)
