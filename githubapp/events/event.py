import os
import re

from github import Consts, Github, GithubIntegration, GithubRetry
from github.Auth import AppAuth, AppUserAuth, Auth, Token
from github.Requester import Requester


class Event:
    """Event base class

    This class represents a generic GitHub webhook event.
    It provides common
    attributes and methods for parsing event data from the request headers and body.
    """

    delivery = None
    github_event = None
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
        Event.github_event = headers["X-Github-Event"]
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
        auth = Event._get_auth()
        self.gh = Github(auth=auth)
        self.requester = Requester(
            auth=auth,
            base_url=Consts.DEFAULT_BASE_URL,
            timeout=Consts.DEFAULT_TIMEOUT,
            user_agent=Consts.DEFAULT_USER_AGENT,
            per_page=Consts.DEFAULT_PER_PAGE,
            verify=True,
            retry=GithubRetry(),
            pool_size=None,
        )

    @staticmethod
    def _get_auth() -> Auth:
        """
        This method is used to get the authentication object for the GitHub API.
        It checks if the environment variables CLIENT_ID, CLIENT_SECRET, and TOKEN are set.
        If they are set, it uses the AppUserAuth object with the CLIENT_ID, CLIENT_SECRET, and TOKEN.
        Otherwise, it uses the AppAuth object with the private key.

        :return: The Auth to be used to authenticate in Github()
        """
        if os.environ.get("CLIENT_ID"):
            return AppUserAuth(
                client_id=os.environ.get("CLIENT_ID"),
                client_secret=os.environ.get("CLIENT_SECRET"),
                token=os.environ.get("TOKEN"),
            )
        if not (private_key := os.getenv("PRIVATE_KEY")):
            with open("private-key.pem", "rb") as key_file:  # pragma no cover
                private_key = key_file.read().decode()
        app_auth = AppAuth(Event.hook_installation_target_id, private_key)
        token = (
            GithubIntegration(auth=app_auth)
            .get_access_token(Event.installation_id)
            .token
        )
        return Token(token)

    @staticmethod
    def normalize_dicts(*dicts) -> dict[str, str]:
        """Normalize the event data to a common format

        Args:
            *dicts: A list of dicts containing the event data

        Returns:
            dict: A dict containing the normalized event data
        """
        union_dict = {}
        for d in dicts:
            for attr, value in d.items():
                attr = attr.lower()
                attr = attr.replace("x-github-", "")
                attr = re.sub(r"[- ]", "_", attr)
                union_dict[attr] = value

        return union_dict

    @classmethod
    def get_event(cls, headers, body) -> type["Event"]:
        """Get the event class based on the event type

        Args:
            headers (dict): The request headers
            body (dict): The request body

        Returns:
            Event: The event class
        """
        event_class = cls
        for event in cls.__subclasses__():
            if event.match(headers, body):
                return event.get_event(headers, body)
        return event_class

    @classmethod
    def match(cls, *dicts):
        """Check if the event matches the event_identifier

        Args:
            *dicts: A list of dicts containing the event data

        Returns:
            bool: True if the event matches the event_identifier, False otherwise
        """
        union_dict = Event.normalize_dicts(*dicts)
        for attr, value in cls.event_identifier.items():
            if not (attr in union_dict and value == union_dict[attr]):
                return False
        return True
