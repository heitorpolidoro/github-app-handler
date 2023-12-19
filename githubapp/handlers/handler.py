import inspect
from collections import defaultdict

from githubapp import SignatureError
from githubapp.Event import Event


class Handler:
    _webhooks = defaultdict(list)

    def __init__(self, name, *args, **kwargs):
        self.name = name

    def root(self):
        return f"{self.name} App up and running!"

    def call_webhook(self, headers, body):
        event = Event.parse_event(headers, body)

        for handler in self._webhooks[event.__class__]:
            handler(event)

    def _register_handler(self, func, event: type[Event]):
        Handler._validate_signature(func)
        self._webhooks[event].append(func)
        for sub_event in event.__subclasses__():
            if issubclass(sub_event, Event):  # pragma: no branch
                self._register_handler(func, sub_event)
        return func

    @staticmethod
    def _validate_signature(func):
        parameters = inspect.signature(func).parameters
        try:
            assert len(parameters) == 1
        except AssertionError:
            signature = ""
            raise SignatureError(func, signature)
