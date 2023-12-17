from github.NamedUser import NamedUser
from github.Repository import Repository

from github_app.Event import Event
from github_app.LazyCompletableGithubObject import LazyCompletableGithubObject


class CreateEvent(Event):
    """This class represents a branch or tag creation event."""

    name = "create"

    def __init__(self, description, master_branch, pusher_type, ref, ref_type, repository, sender, **kwargs):
        super().__init__(**kwargs)
        self.description: str = description
        self.master_branch: str = master_branch
        self.pusher_type: str = pusher_type
        self.ref: str = ref
        self.ref_type: str = ref_type
        self.repository: Repository = LazyCompletableGithubObject.get_lazy_instance(
            Repository, attributes=repository
        )
        self.sender: NamedUser = LazyCompletableGithubObject.get_lazy_instance(
            NamedUser, attributes=sender
        )
