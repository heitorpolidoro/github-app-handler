# import logging
#
# from github import Github
# from github.Auth import AppInstallationAuth
#
#
import re


class Event:
    #     """Event base class
    #
    #     This class represents a generic GitHub webhook event. It provides common
    #     attributes and methods for parsing event data from the request headers and body.
    #
    #     Attributes:
    #         name (str): The name of the event (e.g. 'issue').
    #         action (str): The action that triggered the event (e.g. 'opened').
    #
    #     Methods:
    #         parse_event(headers, body): Parses the event from the request.
    #     """
    #
    #     name = None
    #     action = None
    # app_id = None
    # installation_id = None

    delivery = None
    event = None
    hook_id = None
    hook_installation_target_id = None
    hook_installation_target_type = None
    installation_id = None
    event_identifier = None

    _raw_body = None
    _raw_headers = None

    #
    def __init__(self, headers, **kwargs):
        Event.delivery = headers["X-Github-Delivery"]
        Event.event = headers["X-Github-Event"]
        Event.hook_id = int(headers["X-Github-Hook-Id"])
        Event.hook_installation_target_id = int(
            headers["X-Github-Hook-Installation-Target-Id"]
        )
        Event.hook_installation_target_type = headers[
            "X-Github-Hook-Installation-Target-Type"
        ]
        Event.installation_id = int(kwargs["installation"]["id"])

        Event._raw_headers = headers
        Event._raw_body = kwargs

    @staticmethod
    def normalize_dicts(*dicts) -> dict[str, str]:
        union_dict = {}
        for d in dicts:
            for attr, value in d.items():
                attr = attr.lower()
                attr = attr.replace("x-github-", "")
                attr = re.sub(r"[- ]", "_", attr)
                union_dict[attr] = value

        return union_dict

    @classmethod
    def get_event(cls, headers, body):
        event_class = cls
        for event in cls.__subclasses__():
            if event.match(headers, body):
                return event.get_event(headers, body)
        return event_class

    @classmethod
    def match(cls, *dicts):
        union_dict = Event.normalize_dicts(*dicts)
        for attr, value in cls.event_identifier.items():
            if not (attr in union_dict and value == union_dict[attr]):
                return False
        return True

        # self.hook_id = int(headers["X-Github-Hook-Id"])
        # self.github_event = headers["X-Github-Event"]
        # self.delivery = headers["X-Github-Delivery"]
        # self.hook_installation_target_type = headers[
        #     "X-Github-Hook-Installation-Target-Type"
        # ]
        # self.hook_installation_target_id = int(
        #     headers["X-Github-Hook-Installation-Target-Id"]
        # )
        # Event.app_id = self.hook_installation_target_id
        # Event.installation_id = int(body["installation"]["id"])
        #
        # self._headers = headers
        # self._body = body


#
#     @classmethod
#     def get_event(cls, headers, body):
#         event = headers["X-Github-Event"]
#         action = body.pop("action", None)
#         event_class = next(filter(lambda x: x.name == event, cls.__subclasses__()))
#         action_class = next(
#             filter(lambda x: x.action == action, event_class.__subclasses__()), None
#         )
#         return action_class(headers=headers, **body)
#
#     def __eq__(self, other):
#         return self.__dict__ == other.__dict__
#
#     def __repr__(self):
#         return f"{self.__class__.__name__}({self.__dict__})"
#     # @classmethod
#     # def parse_event(cls, headers, body):
#     #     """Returns an Event classe for the event in webhook"""
#     #     action = body.pop("action", None)
#     #     event_class = cls.get_webhook_class(event, action, body)
#     #     if event_class:
#     #         return event_class(headers=headers, **body)
#     #
#     # @classmethod
#     # def get_webhook_class(cls, event, action, body=None):
#     #     """Returns the webhook class for the event and action in webhook"""
#     #     body = body or {}
#     #     clazz = None
#     #     event_classes = list(filter(lambda x: x.name == event, cls.__subclasses__()))
#     #     if len(event_classes) > 1:
#     #         raise ValueError(f"Multiple webhook classes for '{event}'")
#     #     if len(event_classes) == 1:
#     #         event_class = event_classes[0]
#     #         if action is None:
#     #             clazz = event_class
#     #         else:
#     #             action_classes = list(
#     #                 filter(lambda x: x.action == action, event_class.__subclasses__())
#     #             )
#     #             if len(action_classes) > 1:
#     #                 raise ValueError(f"Multiple webhook classes for '{event}.{action}'")
#     #             if len(action_classes) == 1:
#     #                 clazz = action_classes[0]
#     #
#     #     if clazz:
#     #         if sub_type := getattr(clazz, "sub_type", None):
#     #             sub_type_value = body.get(sub_type)
#     #             for sub_type_class in clazz.__subclasses__():
#     #                 if getattr(sub_type_class, sub_type) == sub_type_value:
#     #                     clazz = sub_type_class
#     #                     break
#     #         return clazz
#     #     event_name = event
#     #     if action:
#     #         event_name += f".{action}"
#     #
#     #     logging.warning(f"No webhook class for '{event_name}'")
