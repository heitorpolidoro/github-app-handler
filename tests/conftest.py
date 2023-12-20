from collections import defaultdict
from unittest.mock import Mock

import pytest

from githubapp.handlers import Handler


@pytest.fixture(autouse=True)
def setup_and_teardown():
    yield
    Handler.handlers = defaultdict(list)


@pytest.fixture
def event_action_request():
    handlers = {
        "X-Github-Event": "event",
        "X-Github-Hook-Id": "1",
        "X-Github-Delivery": "a1b2c3d4",
        "X-Github-Hook-Installation-Target-Type": "type",
        "X-Github-Hook-Installation-Target-Id": "3",
    }
    body = {}
    for txt in [
        "action",
        "release",
        "master_branch",
        "pusher_type",
        "ref",
        "description",
        "comment",
    ]:
        body[txt] = txt
    for obj in ["installation", "repository", "sender", "issue", "changes"]:
        body[obj] = {}

    body["installation"]["id"] = "4"
    yield handlers, body


@pytest.fixture
def method():
    def dummy(event):
        return event

    yield Mock(wraps=dummy)
