import os

from github import GithubIntegration


class Event:
    """Event base class

    This class represents a generic GitHub webhook event. It provides common
    attributes and methods for parsing event data from the request headers and body.

    Attributes:
        name (str): The name of the event (e.g. 'issue').
        action (str): The action that triggered the event (e.g. 'opened').

    Methods:
        parse_event(headers, body): Parses the event from the request.
    """

    name = None
    action = None
    installation_id = None

    def __init__(self, headers, installation):
        self.hook_id = headers["X-Github-Hook-Id"]
        self.name = headers["X-Github-Event"]
        self.delivery_id = headers["X-Github-Delivery"]
        self.hook_installation_target_type = headers[
            "X-Github-Hook-Installation-Target-Type"
        ]
        self.hook_installation_target_id = headers[
            "X-Github-Hook-Installation-Target-Id"
        ]
        Event.installation_id = installation["id"]

    @classmethod
    def parse_event(cls, headers, body):
        """Returns an Event classe for the event in webhook"""
        event = headers["X-Github-Event"]
        action = body.pop("action")
        event_class = cls.get_webhook_class(event, action)
        return event_class(headers=headers, **body)

    @classmethod
    def get_webhook_class(cls, event, action):
        """Returns the webhook class for the event and action in webhook"""
        event_classes = list(filter(lambda x: x.name == event, cls.__subclasses__()))
        if len(event_classes) > 1:
            raise ValueError(f"Multiple webhook classes for '{event}'")
        if len(event_classes) == 1:
            event_class = event_classes[0]
            action_classes = list(
                filter(lambda x: x.action == action, event_class.__subclasses__())
            )
            if len(action_classes) > 1:
                raise ValueError(f"Multiple webhook classes for '{event}.{action}'")
            if len(action_classes) == 1:
                return action_classes[0]

        raise NotImplementedError(f"No webhook class for '{event}.{action}'")
