from github.Issue import Issue
from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject
from githubapp.events.event import Event


class IssuesEvent(Event):
    """This class represents an issue event."""

    event_identifier = {"event": "issues"}

    def __init__(
        self,
        headers,
        issue,
        repository,
        sender,
        **kwargs,
    ):
        super().__init__(headers, **kwargs)
        self.issue = LazyCompletableGithubObject.get_lazy_instance(
            Issue, attributes=issue
        )
        self.repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )


class IssueOpenedEvent(IssuesEvent):
    """This class represents an issue opened event."""

    event_identifier = {"action": "opened"}

    def __init__(
        self,
        headers,
        changes=None,
        **kwargs,
    ):
        super().__init__(headers, **kwargs)
        # changes \/
        self.old_issue = (
            LazyCompletableGithubObject.get_lazy_instance(
                Issue, attributes=changes.get("old_issue")
            )
            if changes
            else None
        )
        self.old_repository = (
            LazyCompletableGithubObject.get_lazy_instance(
                Repository, attributes=changes.get("old_repository")
            )
            if changes
            else None
        )
        # changes /\


class IssueEditedEvent(IssuesEvent):
    """This class represents an issue opened event."""

    event_identifier = {"action": "edited"}

    def __init__(
        self,
        headers,
        changes,
        **kwargs,
    ):
        super().__init__(headers, **kwargs)
        self.changes = changes
