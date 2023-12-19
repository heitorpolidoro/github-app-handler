from flask import Flask as OriginalFlask
from flask import request

from githubapp import (
    CreateBranchEvent,
    CreateEvent,
    CreateTagEvent,
    IssueCommentCreatedEvent,
    IssueCommentDeletedEvent,
    IssueCommentEvent,
    ReleaseEvent,
    ReleaseReleasedEvent,
)
from githubapp.Event import Event
from githubapp.handlers.handler import Handler
from githubapp.IssueCommentEvent import IssueCommentEditedEvent
from githubapp.ReleaseEvent import ReleaseCreatedEvent


# noinspection PyPep8Naming
class Flask(OriginalFlask, Handler):
    """Flask shell to create and handle GitHub webhooks"""

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
        return func

    def Release(self, func):
        self._register_handler(func, ReleaseEvent)
        return func

    def ReleaseReleased(self, func):
        self._register_handler(func, ReleaseReleasedEvent)
        return func

    def ReleaseCreated(self, func):
        self._register_handler(func, ReleaseCreatedEvent)
        return func

    def Create(self, func):
        self._register_handler(func, CreateEvent)
        return func

    def CreateBranch(self, func):
        self._register_handler(func, CreateBranchEvent)
        return func

    def CreateTag(self, func):
        self._register_handler(func, CreateTagEvent)
        return func

    def IssueComment(self, func):
        self._register_handler(func, IssueCommentEvent)
        return func

    def IssueCommentCreated(self, func):
        self._register_handler(func, IssueCommentCreatedEvent)
        return func

    def IssueCommentEdited(self, func):
        self._register_handler(func, IssueCommentEditedEvent)
        return func

    def IssueCommentDeleted(self, func):
        self._register_handler(func, IssueCommentDeletedEvent)
        return func
