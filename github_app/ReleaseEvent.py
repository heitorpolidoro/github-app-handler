from github.GitRelease import GitRelease
from github.NamedUser import NamedUser
from github.Repository import Repository

from github_app.Event import Event
from github_app.LazyCompletableGithubObject import LazyCompletableGithubObject


class ReleaseEvent(Event):
    """This class represents a generic release event."""
    name = "release"

    def __init__(self, release, repository, sender, **kwargs):
        super().__init__(**kwargs)
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
    action = "released"


class ReleaseCreatedEvent(ReleaseEvent):
    """This class represents an event when a release is created."""
    action = "created"
