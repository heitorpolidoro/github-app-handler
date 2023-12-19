from flask import Flask as OriginalFlask, request

from githubapp import ReleaseEvent, ReleaseReleasedEvent, CreateBranchEvent, CreateEvent, IssueCommentEvent, \
    IssueCommentCreatedEvent, IssueCommentDeletedEvent
from githubapp.Event import Event
from githubapp.handlers.handler import Handler


# noinspection PyPep8Naming
class Flask(OriginalFlask, Handler):
    """ Flask shell to create and handle GitHub webhooks """

    def __init__(self, name, *args, **kwargs):
        OriginalFlask.__init__(self, name, *args, **kwargs)
        Handler.__init__(self, name, *args, **kwargs)
        self.route("/", methods=["GET"])(self.root)
        self.route("/", methods=["POST"])(self.webhook)

    def webhook(self):
        body = request.json
        headers = dict(request.headers)
        self.call_webhook(headers, body)
        return "OK"

    def any(self, func):
        self._register_handler(func, Event)

    def Release(self, func):
        self._register_handler(func, ReleaseEvent)

    def ReleaseReleased(self, func):
        self._register_handler(func, ReleaseReleasedEvent)

    def ReleaseCreated(self, func):
        self._register_handler(func, ReleaseReleasedEvent)

    def Create(self, func):
        self._register_handler(func, CreateEvent)

    def CreateBranch(self, func):
        self._register_handler(func, CreateBranchEvent)

    def CreateTag(self, func):
        self._register_handler(func, CreateBranchEvent)

    def IssueComment(self, func):
        self._register_handler(func, IssueCommentEvent)

    def IssueCommentCreated(self, func):
        self._register_handler(func, IssueCommentCreatedEvent)

    def IssueCommentEdited(self, func):
        self._register_handler(func, IssueCommentDeletedEvent)
    def IssueCommentDeleted(self, func):
        self._register_handler(func, IssueCommentDeletedEvent)
