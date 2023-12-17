from github_app.IssueCommentEvent import (
    IssueCommentCreatedEvent, IssueCommentDeletedEvent,
)
from tests.factory import event_factory


def test_issue_comment_created():
    event = event_factory(
        "issue_comment",
        "created",
        add_to_body=["issue", "repository", "sender", "comment"]
    )
    assert isinstance(event, IssueCommentCreatedEvent)


def test_issue_comment_deleted():
    event = event_factory(
        "issue_comment",
        "deleted",
        add_to_body=["issue", "repository", "sender", "comment"]
    )
    assert isinstance(event, IssueCommentDeletedEvent)
