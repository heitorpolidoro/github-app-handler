import os
from datetime import timedelta
from typing import Any, Union

from dateutil.parser import parse
from github import Consts, GithubIntegration, GithubRetry
from github.Auth import AppAuth, AppUserAuth, Token
from github.GithubObject import CompletableGithubObject
from github.Requester import Requester

from githubapp.events.event import Event


class LazyRequester(Requester):
    """
    This class is a lazy version of Requester, which means that it will not make any requests to the API
    until the object is accessed.
    When any attribute of Requester is accessed, initialize the requester.

    """

    def __init__(self):  # skipcq:  PYL-W0231
        self._initialized = False

    def __getattr__(self, item):
        if not self._initialized:
            self._initialized = True
            self.initialize()
            return getattr(self, item)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )

    # noinspection PyMethodMayBeStatic
    def initialize(self):
        """
        Initialize the requester with authentication and default settings.

        This method initializes the requester with the necessary authentication and default settings.

        Raises:
            OSError: If the private key file 'private-key.pem' is not found or cannot be read.
            ValueError: If the private key is not found in the environment variables.

        """
        if os.environ.get("CLIENT_ID"):
            date = parse(os.environ.get("DATE"))

            auth = AppUserAuth(
                client_id=os.environ.get("CLIENT_ID"),
                client_secret=os.environ.get("CLIENT_SECRET"),
                token=os.environ.get("TOKEN"),
                expires_at=date + timedelta(seconds=28800),
                refresh_token=os.environ.get("REFRESH_TOKEN"),
                refresh_expires_at=date + timedelta(seconds=15811200),
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
    ):
        # self._lazy_initialized = False
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
    def get_lazy_instance(clazz, attributes):
        """Makes the clazz a subclass of LazyCompletableGithubObject"""
        return type(clazz.__name__, (LazyCompletableGithubObject, clazz), {})(
            attributes=attributes
        )
