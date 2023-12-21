import re


class Event:
    """
    Base class for representing a generic GitHub webhook event.

    This class provides common attributes and methods for parsing event data from the request headers and body. The attributes include delivery, event, hook_id, hook_installation_target_id, hook_installation_target_type, installation_id, and event_identifier. The methods include __init__, normalize_dicts, get_event, and match.
    """

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
