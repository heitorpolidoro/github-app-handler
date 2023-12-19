import inspect

from flask import Flask as OriginalFlask
from flask import request

from githubapp.Event import Event
from githubapp.handlers.exceptions import SignatureError



def validate_signature(func):
    parameters = inspect.signature(func).parameters
    try:
        assert len(parameters) == 1
    except AssertionError:
        signature = ""
        raise SignatureError(func, signature)


class Flask(OriginalFlask):
    _webhooks_ = {}

    def __init__(self, *args, **kwargs):
        super(Flask, self).__init__(*args, **kwargs)
        self.route("/", methods=["GET"])(self.root)
        self.route("/", methods=["GET"])(self.root)
        self.route("/", methods=["POST"])(self.webhook)

    #
    def root(self):
        return f"{self.name} App up and running!"

    def webhook(self):
        data = request.json
        headers = dict(request.headers)
        event = Event.parse_event(headers, data)

        for key in ["__any__", event.name, f"{event.name}.{event.action}"]:
            if key in self._webhooks_:
                self._webhooks_[key](event)
        return "OK"

    def _register_handler(self, func, event=None, action=None):
        assert (
            action is None or event is not None
        ), "action must be specified with event"
        validate_signature(func)
        key = event
        if action:
            key += f".{action}"

        self._webhooks_[key] = func
        return func

    def any(self, func):
        self._register_handler(func, "__any__")

    def Release(self, func):
        self._register_handler(func, "release")

    def ReleaseReleased(self, func):
        self._register_handler(func, "release", "released")

