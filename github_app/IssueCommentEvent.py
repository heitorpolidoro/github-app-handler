from github.Issue import Issue
from github.IssueComment import IssueComment
from github.NamedUser import NamedUser
from github.Repository import Repository

from github_app.Event import Event
from github_app.LazyCompletableGithubObject import LazyCompletableGithubObject


class IssueCommentEvent(Event):
    name = "issue_comment"

    def __init__(self, comment, issue, repository, sender, **kwargs):
        super().__init__(**kwargs)
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
    action = "created"


class IssueCommentDeletedEvent(IssueCommentEvent):
    action = "deleted"
