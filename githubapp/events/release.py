from github.GitRelease import GitRelease
from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.events.event import Event
from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class ReleaseEvent(Event):
    """This class represents a generic release event."""

    event_identifier = {"event": "release"}

    def __init__(self, headers, release, repository, sender, **kwargs):
        super().__init__(headers, **kwargs)
        self.release: GitRelease = LazyCompletableGithubObject.get_lazy_instance(
            GitRelease, attributes=release
        )
        self.repository: Repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender: NamedUser = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )


class ReleaseReleasedEvent(ReleaseEvent):
    """This class represents an event when a release is released."""

    event_identifier = {"action": "released"}


class ReleaseCreatedEvent(ReleaseEvent):
    """This class represents an event when a release is created."""

    event_identifier = {"action": "created"}
