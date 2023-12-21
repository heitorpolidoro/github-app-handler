import re


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

    _raw_body = None
    _raw_headers = None

    #
    def __init__(self, headers, **kwargs):
        """
        Initialize the Event object with the provided headers and keyword arguments.

        Args:
            headers (dict): A dictionary containing the headers for the event.
            **kwargs: Additional keyword arguments.

        Raises:
            KeyError: If any of the required keys are missing in the headers or kwargs.

        Example:
            To initialize the Event object:
            >>> headers = {
            ...     "X-Github-Delivery": "delivery_id",
            ...     "X-Github-Event": "event_type",
            ...     "X-Github-Hook-Id": "hook_id",
            ...     "X-Github-Hook-Installation-Target-Id": "installation_target_id",
            ...     "X-Github-Hook-Installation-Target-Type": "installation_target_type"
            ... }
            >>> kwargs = {
            ...     "installation": {
            ...         "id": "installation_id"
            ...     }
            ... }
            >>> event = Event(headers, **kwargs)

        """

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
        """
        Check if the given dictionaries match the event identifier of the class.

        Args:
            cls: The class whose event identifier needs to be matched.
            *dicts: Variable number of dictionaries to be checked for a match.

        Returns:
            bool: True if all the dictionaries match the event identifier, False otherwise.

        Raises:
            (if applicable)
            - TypeError: If the input is not of expected type.
            - KeyError: If the required keys are not present in the input dictionaries.

        Example:
            class Example:
                event_identifier = {'key1': 'value1', 'key2': 'value2'}

            dict1 = {'key1': 'value1', 'key2': 'value2'}
            dict2 = {'key1': 'value1', 'key2': 'value3'}

            print(match(Example, dict1, dict2))  # Output: False
        """

        union_dict = Event.normalize_dicts(*dicts)
        for attr, value in cls.event_identifier.items():
            if not (attr in union_dict and value == union_dict[attr]):
                return False
        return True
