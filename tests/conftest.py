from collections import defaultdict
from unittest.mock import Mock, patch

import pytest

from githubapp import webhook_handler


@pytest.fixture(autouse=True)
def setup_and_teardown():
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
    def dummy(event):
        return event

    yield Mock(wraps=dummy)


@pytest.fixture(autouse=True)
def validate_signature():
    with patch(
            "githubapp.webhook_handler._validate_signature",
            return_value=True,
    ):
        yield
