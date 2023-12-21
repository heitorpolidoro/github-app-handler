from .event import Event


class EventGetter:
    @classmethod
    def get_event(cls, headers, body):
        event_class = Event
        for event in Event.__subclasses__():
            if event.match(headers, body):
                return event.get_event(headers, body)
        return event_class
