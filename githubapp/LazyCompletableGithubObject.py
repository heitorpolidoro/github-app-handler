import os
from typing import Any, Union

from github import Consts, GithubIntegration, GithubRetry
from github.Auth import AppAuth, Token
from github.GithubObject import CompletableGithubObject
from github.Requester import Requester

from githubapp.events import Event

def get_requester():
    if not (private_key := os.getenv("PRIVATE_KEY")):
        with open("private-key.pem", "rb") as key_file:  # pragma no cover
            private_key = key_file.read().decode()
    app_auth = AppAuth(Event.hook_installation_target_id, private_key)
    token = (
        GithubIntegration(auth=app_auth)
        .get_access_token(Event.installation_id)
        .token
    )
    Event.app_auth = app_auth
    return Requester(
        auth=Token(token),
        base_url=Consts.DEFAULT_BASE_URL,
        timeout=Consts.DEFAULT_TIMEOUT,
        user_agent=Consts.DEFAULT_USER_AGENT,
        per_page=Consts.DEFAULT_PER_PAGE,
        verify=True,
        retry=GithubRetry(),
        pool_size=None,
    )

class LazyRequester(Requester):
    def __init__(self):
        self._initialized = False

    def __getattr__(self, item):
        if not self._initialized:
            self._initialized = True
            self._requester = get_requester()
        return getattr(self._requester, item)

class LazyCompletableGithubObject(CompletableGithubObject):
    """
    A lazy CompletableGithubObject that will only initialize when it is accessed.
    In the initialization will create a github.Requester.Requester
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
        # self._lazy_initialized = True
        # self._lazy_requester = None
        self._requester = LazyRequester()


    @property
    def lazy_requester(self):
        if self._lazy_requester is None:
            self._lazy_requester = get_requester()
        return self._lazy_requester

    def __getattribute__(self, item):
        #     """If the value is None, makes a request to update the object."""
        value = super().__getattribute__(item)
        if (
                value is None
                and item != "_requester"
                and not self._requester._initialized
        ):
            headers, data = self._requester.requestJsonAndCheck("GET", self.url)
            self.__class__.__init__(self, self._requester, headers, data, completed=False)
            value = super().__getattribute__(item)
        return value
    #     if item == "_requester" and value is None:
    #         self._requester = self.lazy_requester
    #     return value
    #     if (
    #             value is None
    #             and not item.startswith("_lazy")
    #             and getattr(self, "_lazy_initialized", False)
    #             and self._lazy_requester is None
    #     ):
    #         headers, data = self.lazy_requester.requestJsonAndCheck("GET", self.url)
    #         new_self = self.__class__(
    #             self.lazy_requester, headers, data, completed=True
    #         )
    #         self.__dict__.update(new_self.__dict__)
    #         value = super().__getattribute__(item)
    #     return value

    @staticmethod
    def get_lazy_instance(clazz, attributes):
        """Makes the clazz a subclass of LazyCompletableGithubObject"""
        if LazyCompletableGithubObject not in clazz.__bases__:
            clazz.__bases__ = tuple(
                [LazyCompletableGithubObject] + list(clazz.__bases__)
            )
        return clazz(attributes=attributes)
