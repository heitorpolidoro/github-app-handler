import inspect
from collections import defaultdict
from functools import wraps
from typing import Any, Callable

from githubapp.events import Event


class SignatureError(Exception):
    """Exception when the method has a wrong signature"""

    def __init__(self, method: Callable[[Any], Any], signature):
        """
        Initialize the class with the provided method and signature.

        Args:
            method (Callable[[Any], Any]): The method to be initialized.
            signature: The signature of the method.

        Raises:
            None

        Example:
            Example usage:
            ```
            instance = ClassName(method, signature)
            ```
        """

        self.message = (
            f"Method {method.__qualname__}({signature}) signature error. "
            f"The method must accept only one argument of the Event type"
        )


def webhook_handler(event: type[Event]):
    """    Decorator to register a method as a webhook handler.

        The method must accept only one argument of the Event type.

        Args:
            event: The event type to handle.

        Returns:
            A decorator that registers the method as a webhook handler.

        Raises:
            SomeException: An exception that may be raised.

        Example:
            @webhook_handler(SomeEvent)
            def handle_event(event):
                # Handle the event
    """

    def decorator(method):
        """
        Decorator function to add a handler for a specific event.

        Args:
            method: The method to be decorated.

        Raises:
            ValueError: If the event is not valid.

        Example:
            @decorator
            def my_handler(event):
                # Handle the event
                pass
        """

        add_handler(event, method)
        return method

    return decorator


def add_handler(event: type[Event], method: Callable):
    """
    Add a handler for a specific event type.

    The handler must accept only one argument of the Event type.

    Args:
        event (type[Event]): The event type to handle.
        method (Callable): The handler method.

    Raises:
        <ExceptionType>: <Description of the exception raised>

    Example:
        add_handler(MyEvent, my_handler_function)
    """
    if subclasses := event.__subclasses__():
        for sub_event in subclasses:
            add_handler(sub_event, method)
    else:
        _validate_signature(method)
        handlers[event].append(method)



handlers = defaultdict(list)

def handle(headers: dict[str, Any], body: dict[str, Any]):
    """    Handle a webhook request.

        The request headers and body are passed to the appropriate handler methods.

        Args:
            headers: The request headers.
            body: The request body.

        Raises:
            KeyError: If the 'action' key is present in the request body.

        Example:
            handle({'Content-Type': 'application/json'}, {'event_type': 'user_created', 'user_id': 123})
    """

    event_class = Event.get_event(headers, body)
    body.pop("action", None)
    for handler in handlers.get(event_class, []):
        handler(event_class(headers, **body))

def root(name):
    """    Decorator to register a method as the root handler.

        The root handler is called when no other handler is found for the request.

        Args:
            name (str): The name of the root handler.

        Returns:
            function: A decorator that registers the method as the root handler.

        Raises:
            Any exceptions raised by the decorated function.

        Example:
            @root('my_root_handler')
            def my_handler():
                return 'Handler executed'
    """

    def root_wrapper():
        """
        Return a string indicating that the application is up and running.

        Raises:
            (Exception): If the 'name' variable is not defined.

        Example:
            >>> name = "MyApp"
            >>> root_wrapper()
            'MyApp App up and running!'
        """

        return f"{name} App up and running!"

    return wraps(root_wrapper)(root_wrapper)


def _validate_signature(method: Callable[[Any], Any]):
    """    Exception raised for errors in method signature.

        Attributes:
            method -- The method with the wrong signature
            signature -- The incorrect signature
    """

    parameters = inspect.signature(method).parameters
    try:
        assert len(parameters) == 1
    except AssertionError:
        signature = ""
        raise SignatureError(method, signature)
