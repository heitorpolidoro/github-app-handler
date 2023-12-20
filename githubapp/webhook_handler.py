import inspect
from collections import defaultdict
from functools import wraps
from typing import Any, Callable

from githubapp.events import Event


class SignatureError(Exception):
    """Exception when the method has a wrong signature"""

    def __init__(self, method, signature):
        self.message = (
            f"Method {method.__qualname__}({signature}) signature error. "
            f"The method must accept only one argument of the Event type"
        )


def webhook_handler(event: type[Event]):
    def decorator(method):
        WebhookHandler.add_handler(event, method)
        return method

    return decorator


class WebhookHandler:
    handlers = defaultdict(list)

    @staticmethod
    def add_handler(event: type[Event], method: Callable):
        if subclasses := event.__subclasses__():
            for sub_event in subclasses:
                WebhookHandler.add_handler(sub_event, method)
        else:
            WebhookHandler.handlers[event].append(method)

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
        for handler in WebhookHandler.handlers.get(event_class, []):
            handler(event_class(headers, **body))

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
