from github.GitRelease import GitRelease
from github.Issue import Issue
from github.IssueComment import IssueComment
from github.NamedUser import NamedUser
from github.Repository import Repository

from github_app.Event import Event
from github_app.LazyCompletableGithubObject import LazyCompletableGithubObject


class ReleaseEvent(Event):
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
    action = "released"


class ReleaseCreatedEvent(ReleaseEvent):
    action = "created"
