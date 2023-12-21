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
    """Decorator to register a method as a webhook handler.

    The method must accept only one argument of the Event type.

    Args:
        event: The event type to handle.

    Returns:
        A decorator that registers the method as a webhook handler.

    Raises:
        None

    Example:
        @webhook_handler(MyEvent)
        def my_event_handler(event):
            # Handle the event
            pass
    """

    def decorator(method):
        WebhookHandler.add_handler(event, method)
        return method

    return decorator


class WebhookHandler:
    """Class to handle webhook requests.

    The WebhookHandler class provides a method to register webhook handlers and a method to handle webhook requests.

    Attributes:
        handlers: A dictionary of event types to lists of handlers.
    """

    handlers = defaultdict(list)

    @staticmethod
    def add_handler(event: type[Event], method: Callable):
        """Add a handler for a specific event type.

        The handler must accept only one argument of the Event type.

        Args:
            event: The event type to handle.
            method: The handler method.

        Raises:
            TypeError: If the handler method does not accept exactly one argument of the Event type.

        Example:
            add_handler(MyEventType, my_handler_method)
        """
        if subclasses := event.__subclasses__():
            for sub_event in subclasses:
                WebhookHandler.add_handler(sub_event, method)
        else:
            WebhookHandler._validate_signature(method)
            WebhookHandler.handlers[event].append(method)

    @staticmethod
    def handle(headers: dict[str, Any], body: dict[str, Any]):
        """Handle a webhook request.

        The request headers and body are passed to the appropriate handler methods.

        Args:
            headers: The request headers.
            body: The request body.

        Raises:
            Any exceptions raised by the handler methods.

        Example:
            handle({'Content-Type': 'application/json'}, {'action': 'create', 'data': {'id': 123}})
        """

        event_class = Event.get_event(headers, body)
        body.pop("action", None)
        for handler in WebhookHandler.handlers.get(event_class, []):
            handler(event_class(headers, **body))

    @staticmethod
    def root(name):
        """Decorator to register a method as the root handler.

        The root handler is called when no other handler is found for the request.

        Args:
            name (str): The name of the root handler.

        Returns:
            function: A decorator that registers the method as the root handler.

        Raises:
            (Exception): Any exceptions that may occur during the execution of the decorated function.

        Example:
            @root("my_root_handler")
            def my_handler():
                return "Handling the request"

        """

        def root_wrapper():
            return f"{name} App up and running!"

        return wraps(root_wrapper)(root_wrapper)

    @staticmethod
    def _validate_signature(method):
        """Validate the signature of a webhook handler method.

        The method must accept only one argument of the Event type.

        Args:
            method: The method to validate.

        Raises:
            SignatureError: If the method has a wrong signature.

        Example:
            >>> class Event:
            ...     pass
            >>> def handler(event: Event):
            ...     pass
            >>> _validate_signature(handler)

        """

        parameters = inspect.signature(method).parameters
        try:
            assert len(parameters) == 1
        except AssertionError:
            signature = ""
            raise SignatureError(method, signature)
