from github.Issue import Issue
from github.IssueComment import IssueComment
from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.events.event import Event
from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class IssueCommentEvent(Event):
    """This class represents a generic issue comment event."""

    event_identifier = {"event": "issue_comment"}

    def __init__(self, headers, comment, issue, repository, sender, **kwargs):
        super().__init__(headers, **kwargs)
        self.issue: Issue = LazyCompletableGithubObject.get_lazy_instance(
            Issue, attributes=issue
        )
        self.issue_comment: IssueComment = (
            LazyCompletableGithubObject.get_lazy_instance(
                IssueComment, attributes=comment
            )
        )
        self.repository: Repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender: NamedUser = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )


class IssueCommentCreatedEvent(IssueCommentEvent):
    """This class represents an event when a comment in an Issue is created."""

    event_identifier = {"action": "created"}


class IssueCommentDeletedEvent(IssueCommentEvent):
    """This class represents an event when a comment in an Issue is deleted."""

    event_identifier = {"action": "deleted"}


class IssueCommentEditedEvent(IssueCommentEvent):
    """This class represents an event when a comment in an Issue is edited."""

    event_identifier = {"action": "edited"}

    def __init__(self, headers, changes, *args, **kwargs):
        super().__init__(headers, *args, **kwargs)
        self.changes = changes
