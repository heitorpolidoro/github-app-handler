from flask import Flask as OriginalFlask, request

from githubapp.handlers import Handler


# from flask import request
#
# from githubapp import (
#     CreateBranchEvent,
#     CreateEvent,
#     CreateTagEvent,
#     IssueCommentCreatedEvent,
#     IssueCommentDeletedEvent,
#     IssueCommentEvent,
#     ReleaseEvent,
#     ReleaseReleasedEvent,
# )
# from githubapp.Event import Event
# from githubapp.handlers.handler_old import Handler
# from githubapp.events.issue_comment import IssueCommentEditedEvent
# from githubapp.ReleaseEvent import ReleaseCreatedEvent
# from githubapp.handlers.handler_manager import HandleManager
# from githubapp.handlers.handler import ReleaseHandler
# from githubapp.webhooks import ReleaseWebhook, Webhook
#
#
# # noinspection PyPep8Naming
class Flask(OriginalFlask):
    """Flask shell to create and handle GitHub webhooks"""

    #
    def __init__(self, name, *args, **kwargs):
        OriginalFlask.__init__(self, name, *args, **kwargs)
        #         Handler.__init__(self, name, *args, **kwargs)
        self.route("/", methods=["GET"])(Handler.root(name))
        self.route("/", methods=["POST"])(Flask.handle_webhook)

    #         self.release = ReleaseHandler()

    @staticmethod
    def handle_webhook():
        headers = dict(request.headers)
        body = request.json
        Handler.handle(headers, body)
        return "OK"


#
# def webhook(self):
#         self.handle_webhook(headers, body)
#         return "OK"
#
#     @staticmethod
#     def any(func):
#         return Webhook()(func)
