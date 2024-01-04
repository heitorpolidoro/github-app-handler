from typing import Optional

from github.Commit import Commit
from github.GitCommit import GitCommit
from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.events.event import Event
from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class PushEvent(Event):
    """This class represents a push event."""

    event_identifier = {"event": "push"}

    def __init__(
        self,
        headers,
        after,
        base_ref,
        before,
        commits,
        compare,
        created,
        deleted,
        forced,
        head_commit,
        pusher,
        ref,
        repository,
        sender,
        **kwargs,
    ):
        super().__init__(headers, **kwargs)
        self.after: str = after
        self.base_ref: Optional[str] = base_ref
        self.before: str = before
        self.commits = [
            LazyCompletableGithubObject.get_lazy_instance(GitCommit, attributes=commit)
            for commit in commits
        ]
        self.compare: str = compare
        self.created: bool = bool(created)
        self.deleted: bool = bool(deleted)
        self.forced: bool = bool(forced)
        self.head_commit = LazyCompletableGithubObject.get_lazy_instance(
            Commit, attributes=head_commit
        )
        self.pusher = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=pusher
        )
        self.ref: str = ref
        self.repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )
