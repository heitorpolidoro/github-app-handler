"""
LazyCompletableGithubObject

This module provides lazy implementations of Github objects that make API
requests only when attributes are accessed.

The LazyRequester class lazily initializes a Requester instance to avoid
making unnecessary requests. Objects that inherit from
LazyCompletableGithubObject will have attributes populated lazily.

Example:

    lazy_obj = LazyCompletableGithubObject.get_lazy_instance(Repo, id=123)
    print(lazy_obj.name) # Makes API request here to get name
"""
import os
from typing import Any, TypeVar, Union

from github import Consts, GithubIntegration, GithubRetry
from github.Auth import AppAuth, AppUserAuth, Token
from github.GithubObject import CompletableGithubObject
from github.Requester import Requester

from githubapp.events.event import Event

T = TypeVar("T")


class LazyRequester(Requester):
    """
    This class is a lazy version of the Requester class. It does not make any requests to the API
    until the object is accessed.
    When any attribute of Requester is accessed, the requester is initialized.
    """

    # noinspection PyMissingConstructor
    def __init__(self) -> None:
        self._initialized = False

    def __getattr__(self, item: str) -> Any:
        if not self._initialized:
            self._initialized = True
            self.initialize()
            return getattr(self, item)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )

    # noinspection PyMethodMayBeStatic
    def initialize(self) -> None:
        """
        Initialize the requester with authentication and default settings.

        This method initializes the requester with the necessary authentication and default settings.

        Raises:
            OSError: If the private key file 'private-key.pem' is not found or cannot be read.
            ValueError: If the private key is not found in the environment variables.

        """
        if os.environ.get("CLIENT_ID"):
            auth = AppUserAuth(
                client_id=os.environ.get("CLIENT_ID"),
                client_secret=os.environ.get("CLIENT_SECRET"),
                token=os.environ.get("TOKEN"),
            )

        else:
            if not (private_key := os.getenv("PRIVATE_KEY")):
                with open("private-key.pem", "rb") as key_file:  # pragma no cover
                    private_key = key_file.read().decode()
            app_auth = AppAuth(Event.hook_installation_target_id, private_key)
            token = (
                GithubIntegration(auth=app_auth)
                .get_access_token(Event.installation_id)
                .token
            )
            auth = Token(token)
        Requester.__init__(
            self,
            auth=auth,
            base_url=Consts.DEFAULT_BASE_URL,
            timeout=Consts.DEFAULT_TIMEOUT,
            user_agent=Consts.DEFAULT_USER_AGENT,
            per_page=Consts.DEFAULT_PER_PAGE,
            verify=True,
            retry=GithubRetry(),
            pool_size=None,
        )


class LazyCompletableGithubObject(CompletableGithubObject):
    """
    This class is a lazy version of CompletableGithubObject, which means that it will not make any requests to the API
    until the object is accessed.
    When initialized, set a LazyRequester as the requester.
    When any value is None, initialize the requester and update self with the data from the API.
    """

    def __init__(
        self,
        requester: "Requester" = None,
        headers: dict[str, Union[str, int]] = None,
        attributes: dict[str, Any] = None,
        completed: bool = False,
    ) -> None:
        if attributes.get("url", "").startswith("https://github"):
            attributes["url"] = attributes["url"].replace("https://github.com", "https://api.github.com/repos")
        #     attributes["url"] = attributes["url"].replace("/commit/", "/commits/")
        # if isinstance(self, GitCommit):
        #     attributes["sha"] = attributes["id"]
        # noinspection PyTypeChecker
        CompletableGithubObject.__init__(
            self,
            requester=requester,
            headers=headers or {},
            attributes=attributes,
            completed=completed,
        )
        self._requester = LazyRequester()

    @staticmethod
    def get_lazy_instance(clazz: type[T], attributes: dict[str, Any]) -> T:
        if attributes is None:
            return None
        """Makes the clazz a subclass of LazyCompletableGithubObject"""
        return type(clazz.__name__, (LazyCompletableGithubObject, clazz), {})(
            attributes=attributes
        )
