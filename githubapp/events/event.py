import re

from .dict_normalizer import DictNormalizer
from .event_getter import EventGetter
from .event_matcher import EventMatcher


class Event:
    """Event base class

    This class represents a generic GitHub webhook event.
    It provides common
    attributes and methods for parsing event data from the request headers and body.
    """

    delivery = None
    event = None
    hook_id = None
    hook_installation_target_id = None
    hook_installation_target_type = None
    installation_id = None
    event_identifier = None

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

    # Methods or logic from DictNormalizer, EventGetter, and EventMatcher will be used directly here

    _raw_body = None
    _raw_headers = None

    #
