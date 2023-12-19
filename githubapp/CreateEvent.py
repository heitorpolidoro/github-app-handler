from github.NamedUser import NamedUser
from github.Repository import Repository

from githubapp.Event import Event
from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class CreateEvent(Event):
    """This class represents a branch or tag creation event."""

    name = "create"
    sub_type = "ref_type"  # TODO comment

    def __init__(
        self,
        description,
        master_branch,
        pusher_type,
        ref,
        ref_type,
        repository,
        sender,
        **kwargs,
    ):
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


class CreateBranchEvent(CreateEvent):
    """This class represents a branch creation event."""

    ref_type = "branch"


class CreateTagEvent(CreateEvent):
    """This class represents a tag creation event."""

    ref_type = "tag"