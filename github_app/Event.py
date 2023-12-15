import os

from github import GithubIntegration


def requester(_):
    if Event._requester is None:
        integration = GithubIntegration(681139, os.getenv("PRIVATE_KEY"))
        Event._requester = integration.get_app()._requester
    return Event._requester


class Event:
    name = None
    action = None
    _requester = None

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
        self.installation_id = installation["id"]

    @classmethod
    def parse_event(cls, headers, body):
        event = headers["X-Github-Event"]
        action = body.pop("action")
        event_class = cls.get_webhook_class(event, action)
        return event_class(headers=headers, **body)

    @classmethod
    def get_webhook_class(cls, event, action):
        for event_class in cls.__subclasses__():
            if event_class.name == event:
                for action_class in event_class.__subclasses__():
                    if action_class.action == action:
                        return action_class

        raise NotImplementedError(f"No webhook class for '{event}.{action}'")
