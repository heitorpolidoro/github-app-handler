import pytest

from github_app.Event import Event
from github_app.IssueCommentEvent import (
    IssueCommentCreatedEvent,
    IssueCommentDeletedEvent,
)

# pytest.register_assert_rewrite("tests.helper")
from tests.helper import assert_event, get_webhook_request


@pytest.mark.vcr
def test_issue_comment_created():
    headers, body = get_webhook_request("issue_comment", "created")
    event = Event.parse_event(headers, body)
    assert isinstance(event, IssueCommentCreatedEvent)
    assert event.name == "issue_comment"
    assert event.action == "created"

    assert_event(event)


@pytest.mark.vcr
def test_issue_comment_deleted():
    headers, body = get_webhook_request("issue_comment", "deleted")
    event = Event.parse_event(headers, body)
    assert isinstance(event, IssueCommentDeletedEvent)
    assert event.name == "issue_comment"
    assert event.action == "deleted"

    assert_event(event)
