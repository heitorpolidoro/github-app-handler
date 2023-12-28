import inspect
from collections import defaultdict
from functools import wraps
from typing import Any, Callable

from githubapp.events.event import Event


class SignatureError(Exception):
    """Exception when the method has a wrong signature"""

    def __init__(self, method: Callable[[Any], Any], signature):
        """
        Args:
        method (Callable): The method to be validated.
        signature: The signature of the method.
        """
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
    """

    def decorator(method):
        """Register the method as a handler for the event"""
        add_handler(event, method)
        return method

    return decorator


def add_handler(event: type[Event], method: Callable):
    """Add a handler for a specific event type.

    The handler must accept only one argument of the Event type.

    Args:
        event: The event type to handle.
        method: The handler method.
    """
    if subclasses := event.__subclasses__():
        for sub_event in subclasses:
            add_handler(sub_event, method)
    else:
        _validate_signature(method)
        handlers[event].append(method)


handlers = defaultdict(list)


def handle(headers: dict[str, Any], body: dict[str, Any]):
    """Handle a webhook request.

    The request headers and body are passed to the appropriate handler methods.

    Args:
        headers: The request headers.
        body: The request body.
    """
    event_class = Event.get_event(headers, body)
    body.pop("action", None)
    for handler in handlers.get(event_class, []):
        handler(event_class(headers, **body))


def root(name):
    """Decorator to register a method as the root handler.

    The root handler is called when no other handler is found for the request.

    Args:
        name: The name of the root handler.

    Returns:
        A decorator that registers the method as the root handler.
    """

    def root_wrapper():
        """A wrapper function to return a default home screen for all Apps"""
        return f"{name} App up and running!"

    return wraps(root_wrapper)(root_wrapper)


def _validate_signature(method: Callable[[Any], Any]):
    """Validate the signature of a webhook handler method.

    The method must accept only one argument of the Event type.

    Args:
        method: The method to validate.

    Raises:
        SignatureError: If the method has a wrong signature.
    """
    parameters = inspect.signature(method).parameters
    if len(parameters) != 1:
        signature = ", ".join(parameters.keys())
        raise SignatureError(method, signature)
