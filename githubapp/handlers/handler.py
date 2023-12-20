import inspect
from collections import defaultdict
from functools import wraps
from typing import Callable, Any

from githubapp.events import Event
from githubapp.handlers import SignatureError


#
# from githubapp import ReleaseEvent
# from githubapp.Event import Event
#
#
class Handler:
    handlers = defaultdict(list)

    @staticmethod
    def add_handler(event: type[Event], method: Callable):
        if subclasses := event.__subclasses__():
            for sub_event in subclasses:
                Handler.add_handler(sub_event, method)
        else:
            Handler.handlers[event].append(method)

    @staticmethod
    def handle(headers: dict[str, Any], body: dict[str, Any]):
        event_class = Event.get_event(headers, body)
        # event = headers["X-Github-Event"]
        # action = body.pop("action", None)
        #
        # event_class = next(filter(lambda e: e.event == event, Event.__subclasses__()))
        #
        # event_class = next(
        #     filter(lambda x: x.action == action, event_class.__subclasses__()), None
        # )
        body.pop("action", None)
        for handler in Handler.handlers.get(event_class, []):
            handler(event_class(headers, body))

    @staticmethod
    def root(name):
        def root_wrapper():
            return f"{name} App up and running!"
        return wraps(root_wrapper)(root_wrapper)

    @staticmethod
    def _validate_signature(method):
        parameters = inspect.signature(method).parameters
        try:
            assert len(parameters) == 1
        except AssertionError:
            signature = ""
            raise SignatureError(method, signature)

    # def webhook(self):
    #     body = request.json
    #     headers = dict(request.headers)
    #     self.handle_webhook(headers, body)
    #     return "OK"


#     event = None
#
#     @classmethod
#     def __call__(cls, handler):
#         if sub_handlers := cls.__subclasses__():
#             for sub_handler in sub_handlers:
#                 sub_handler()(handler)
#         else:
#             cls.handlers[cls.event].append(handler)
#
#     @classmethod
#     def handle(cls, headers, body):
#         if event := Event.get_event(headers, body):
#             for handler in cls.handlers[event.__class__]:
#                 handler(event)
#
#
#
# class ReleaseHandler(Handler):
#     event = ReleaseEvent
#
