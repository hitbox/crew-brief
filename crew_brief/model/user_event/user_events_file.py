from crew_brief.mixin import ItemMixin

class UserEventsFile(ItemMixin):

    def __init__(self, legIdentifier, userId, userEvents):
        """
        :param legIdentifier:
            Dict of leg identifying data.
        :param userId:
            String or int identifying the user.
        :param userEvents:
            List of UserEvent objects.
        """
        self.legIdentifier = legIdentifier
        self.userId = userId
        self.userEvents = userEvents

    def __excel__(self):
        data = {
            'legIdentifier': self.legIdentifier,
            'userId': self.userId,
        }
        data['userEvents'] = [user_event.__excel__() for user_event in self.userEvents]
        return self.__class__(**data)
