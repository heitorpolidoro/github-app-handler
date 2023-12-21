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

    
    dict_normalizer = DictNormalizer()
    event_getter = EventGetter()
    event_matcher = EventMatcher()

    _raw_body = None
    _raw_headers = None

    def __init__(self, data_parser):
        self.data_parser = data_parser
    #
