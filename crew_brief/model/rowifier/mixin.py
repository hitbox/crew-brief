class ConsistencyMixin:

    def event_lists_are_consistent(self, user_events1, user_events2):
        """
        Check if the truthiness of userEvents is the same for both lists.
        """
        return bool(user_events1) == bool(user_events2)
