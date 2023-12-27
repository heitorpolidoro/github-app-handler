from typing import Optional

from github.Branch import Branch
from github.GitCommit import GitCommit
from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject
from githubapp.events import Event


class StatusEvent(Event):
    """This class represents a branch or tag creation event."""

    event_identifier = {"event": "status"}

    def __init__(
        self,
        headers,
        branches,
        commit,
        context,
        created_at,
        description,
        id,
        name,
        repository,
        sender,
        sha,
        state,
        target_url,
        updated_at,
        **kwargs,
    ):
        super().__init__(headers, **kwargs)
        self.branches: list[Branch] = [
            LazyCompletableGithubObject.get_lazy_instance(Repository, attributes=branch)
            for branch in branches
        ]
        self.commit: GitCommit = LazyCompletableGithubObject.get_lazy_instance(
            GitCommit, attributes=commit
        )
        self.context: str = context
        self.created_at: str = created_at
        self.description: Optional[str] = description
        self.id: int = id
        self.name: str = name
        self.repository: Repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender: NamedUser = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )
        self.sha: str = sha
        self.state: str = state  # TODO Enum
        self.target_url: Optional[str] = target_url
        self.updated_at: str = updated_at
