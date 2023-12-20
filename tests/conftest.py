from collections import defaultdict
from unittest.mock import Mock

import pytest

from githubapp.webhook_handler import WebhookHandler


@pytest.fixture(autouse=True)
def setup_and_teardown():
    yield
    WebhookHandler.handlers = defaultdict(list)


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
