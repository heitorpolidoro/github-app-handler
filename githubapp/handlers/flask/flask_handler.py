import inspect

from flask import Flask as OriginalFlask
from flask import request

from githubapp.Event import Event
from githubapp.handlers.exceptions import SignatureError

# from githubapp_utils.models import Hook, IssuesHook
# from githubapp_utils.webhooks import IssuesWebhooks
#
# def compare_dicts(dict1, dict2):
#     def normalize_key(key):
#         return key.replace("GitHub", "Github").replace("ID", "Id")
#     dict1 = {normalize_key(k): v for k, v in dict1.items()}
#     dict2 = {normalize_key(k): v for k, v in dict2.items()}
#     # Print keys only in dict1
#     only_in_dict1 = {k: dict1[k] for k in set(dict1) - set(dict2)}
#     print('Keys only in first dict:', only_in_dict1)
#
#     # Print keys only in dict2
#     only_in_dict2 = {k: dict2[k] for k in set(dict2) - set(dict1)}
#     print('Keys only in second dict:', only_in_dict2)
#
#     # Print keys in both dicts but values differ
#     both_but_different = {k: (dict1[k], dict2[k]) for k in set(dict1) & set(dict2)
#                           if dict1[k] != dict2[k]}
#
#     for d1, d2 in both_but_different.values():
#         if isinstance(d1, dict) and isinstance(d2, dict):
#             compare_dicts(d1, d2)
#         else:
#             print("different values", d1, d2)


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
        # self.issues = IssuesWebhooks(self)

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
        #     output = {
        #         'guid': head['X-Github-Delivery'],
        #         'delivered_at': data['issue']['created_at'],
        #         'event': head['X-Github-Event'],
        #         'action': data['action'],
        #         'installation_id': data['installation']['id'],
        #         'repository_id': data['repository']['id'],
        #         'url': data['issue']['url'],
        #         'request': {
        #             'headers': head,  # Your input data here
        #             'payload': data  # Your input data here
        #         },
        #     }
        #     h = HookDelivery(None, {}, output, True)
        #
        #     print(h.event, h.action)
        #     hook: Union[Hook, IssuesHook] = Hook(headers=request.headers, **request.json)
        #     assert hook._extra_args == {}
        #
        #     if func := self._webhooks_.get(f"{hook.event}.{hook.action}") or self._webhooks_.get(hook.event):
        #         func(hook)
        return "OK"

    def _register_handler(self, func, event=None, action=None):
        if not (action is None or event is not None):
            raise AssertionError("action must be specified with event")
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

    #
    # @staticmethod
    # def clear_and_call(f: Callable):
    #     @wraps(f)
    #     def wrapper(hook):
    #         try:
    #             params = {}
    #             for param in inspect.signature(f).parameters.values():
    #                 params[param.name] = getattr(hook, param.name)
    #             return f(**params)
    #         except AttributeError as e:
    #             raise AttributeError(
    #                 f"{e}, check https://docs.github.com/en/webhooks/webhook-events-and-payload")
    #
    #     return wrapper
    #
    # def add_webhook_call(self, webhook_name: str, f: Callable):
    #     self._webhooks_[webhook_name] = self.clear_and_call(f)
    #     return f
