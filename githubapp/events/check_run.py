from github.CheckRun import CheckRun
from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject
from githubapp.events.event import Event


class CheckRunEvent(Event):
    """This class represents an issue event."""

    event_identifier = {"event": "check_run"}

    def __init__(
            self,
            headers,
            check_run,
            repository,
            sender,
            **kwargs,
    ):
        super().__init__(headers, **kwargs)
        self.check_run = LazyCompletableGithubObject.get_lazy_instance(
            CheckRun, attributes=check_run
        )
        self.repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )


class CheckRunCompletedEvent(CheckRunEvent):
    """This class represents an issue event."""

    event_identifier = {"action": "completed"}

