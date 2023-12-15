import pytest
import vcr

from github_app.Event import Event
from github_app.IssueCommentEvent import (
    IssueCommentCreatedEvent,
    IssueCommentDeletedEvent,
)
from github_app.ReleaseEvent import ReleaseReleasedEvent

from tests.helper import assert_event, get_webhook_request

@pytest.mark.vcr
def test_release_released():
    headers, body = get_webhook_request("release", "released")
    event = Event.parse_event(headers, body)
    assert isinstance(event, ReleaseReleasedEvent)
    assert event.name == "release"
    assert event.action == "released"

    assert_event(event)
