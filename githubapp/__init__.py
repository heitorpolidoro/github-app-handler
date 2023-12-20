# import logging
#
# from githubapp.events.create import CreateBranchEvent, CreateEvent, CreateTagEvent
# from githubapp.handlers.exceptions import SignatureError
# from githubapp.events.issue_comment import (
#     IssueCommentCreatedEvent,
#     IssueCommentDeletedEvent,
#     IssueCommentEvent,
# )
# from githubapp.ReleaseEvent import ReleaseEvent, ReleaseReleasedEvent
#
# logging.basicConfig(
#     format="%(levelname)s:%(module)s:%(funcName)s:%(message)s", level=logging.INFO
# )
# try:
#     from githubapp.handlers.flask.flask_handler import Flask
# except ImportError:  # pragma no cover
#
#     def Flask(*_args, **_kwargs):
#         print(
#             "To use Flask along with GithubAppHandler, install flask (pip install flask)"
#             " or the GithubAppHandler flask version (pip install github-app-handler[flask])"
#         )
#
#
__version__ = "0.0.5"
#
# __all__ = [
#     "CreateEvent",
#     "CreateBranchEvent",
#     "CreateTagEvent",
#     "IssueCommentEvent",
#     "IssueCommentCreatedEvent",
#     "IssueCommentDeletedEvent",
#     "ReleaseEvent",
#     "ReleaseReleasedEvent",
#     "SignatureError",
#     "Flask",
# ]
