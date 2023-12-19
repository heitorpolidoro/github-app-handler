from githubapp.IssueCommentEvent import (
    IssueCommentCreatedEvent,
    IssueCommentDeletedEvent,
    IssueCommentEditedEvent,
)
from tests.factory import event_factory


def test_issue_comment_created():
    event = event_factory(
        "issue_comment",
        "created",
        add_to_body=["issue", "repository", "sender", "comment"],
    )
    assert isinstance(event, IssueCommentCreatedEvent)


def test_issue_comment_deleted():
    event = event_factory(
        "issue_comment",
        "deleted",
        add_to_body=["issue", "repository", "sender", "comment"],
    )
    assert isinstance(event, IssueCommentDeletedEvent)


def test_issue_comment_edited():
    event = event_factory(
        "issue_comment",
        "edited",
        add_to_body=["issue", "repository", "sender", "comment", "changes"],
    )
    assert isinstance(event, IssueCommentEditedEvent)
