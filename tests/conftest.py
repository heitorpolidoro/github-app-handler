from collections import defaultdict
from unittest.mock import Mock, patch

import pytest

from githubapp import webhook_handler


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    This function sets up and tears down the environment.

    Yields:
        None

    Raises:
        No exceptions are raised.

    Example:
        setup_and_teardown()
    """

    yield
    webhook_handler.handlers = defaultdict(list)


@pytest.fixture
def event_action_request():
    handlers = {
        "X-Github-Event": "event",
        "X-Github-Hook-Id": "1",
        "X-Github-Delivery": "a1b2c3d4",
        "X-Github-Hook-Installation-Target-Type": "type",
        "X-Github-Hook-Installation-Target-Id": "2",
    }
    body = {"installation": {"id": "3"}, "action": "action"}
    yield handlers, body


@pytest.fixture
def method():
    """
    This function yields a Mock object that wraps the 'dummy' function.

    Returns:
        Mock: A Mock object that wraps the 'dummy' function.

    Raises:
        This function does not raise any exceptions.

    Example:
        Example usage of the 'method' function:
        ```
        result = method()
        ```
    """

    def dummy(event):
        return event

    yield Mock(wraps=dummy)


@pytest.fixture(autouse=True)
def validate_signature():
    """
    Validate the signature.

    This function validates the signature using the _validate_signature method from webhook_handler module.

    Raises:
        None

    Example:
        validate_signature()
    """

    with patch(
        "githubapp.webhook_handler._validate_signature",
        return_value=True,
    ):
        yield
