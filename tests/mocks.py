from githubapp.events.event import Event


class EventTest(Event):
    """ Event class for tests """
    event_identifier = {"event": "event"}


class SubEventTest(EventTest):
    """ SubEvent class for tests """
    event_identifier = {"action": "action"}
