from githubapp.events import Event


class EventTest(Event):
    event_identifier = {"event": "event"}


class SubEventTest(EventTest):
    event_identifier = {"action": "action"}
