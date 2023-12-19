from githubapp.CreateEvent import CreateBranchEvent, CreateEvent, CreateTagEvent
from githubapp.handlers.exceptions import SignatureError
from githubapp.IssueCommentEvent import (
    IssueCommentCreatedEvent,
    IssueCommentDeletedEvent,
    IssueCommentEvent,
)
from githubapp.ReleaseEvent import ReleaseEvent, ReleaseReleasedEvent

try:
    from githubapp.handlers.flask.flask_handler import Flask
except ImportError:  # pragma no cover

    def Flask(*_args, **_kwargs):
        print(
            "To use Flask along with GithubAppHandler, install flask (pip install flask)"
            " or the GithubAppHandler flask version (pip install GithubAppHandler[flask])"
        )


__version__ = "0.0.1"

__all__ = [
    "CreateEvent",
    "CreateBranchEvent",
    "CreateTagEvent",
    "IssueCommentEvent",
    "IssueCommentCreatedEvent",
    "IssueCommentDeletedEvent",
    "ReleaseEvent",
    "ReleaseReleasedEvent",
    "SignatureError",
    "Flask",
]
