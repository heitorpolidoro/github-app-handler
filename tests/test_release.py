from github_app import ReleaseReleasedEvent
from github_app.IssueCommentEvent import (
    IssueCommentCreatedEvent,
    IssueCommentDeletedEvent,
)
from github_app.ReleaseEvent import ReleaseCreatedEvent
from tests.factory import event_factory


def test_release_released():
    event = event_factory(
        "release", "released", add_to_body=["release", "repository", "sender"]
    )
    assert isinstance(event, ReleaseReleasedEvent)


def test_release_created():
    event = event_factory(
        "release", "created", add_to_body=["release", "repository", "sender"]
    )
    assert isinstance(event, ReleaseCreatedEvent)
