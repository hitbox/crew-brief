from crew_brief.mixin import ItemMixin

from .event_detail import EventDetail

class UserEvent(ItemMixin):

    def __init__(self, eventTimeStamp, eventType, status, eventDetails):
        self.eventTimeStamp = eventTimeStamp
        self.eventType = eventType
        self.status = status
        self.eventDetails = EventDetail(eventDetails)

    def __excel__(self):
        data = {
            'eventTimeStamp': self.eventTimeStamp,
            'eventType': self.eventType,
            'status': self.status,
        }
        data['eventDetails'] = self.eventDetails.__excel__()
        return self.__class__(**data)
