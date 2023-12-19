import os
from typing import Any, Union

from github import Consts, GithubIntegration, GithubRetry
from github.Auth import AppAuth, Token
from github.GithubObject import CompletableGithubObject
from github.Requester import Requester

from githubapp.Event import Event


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
        completed: bool = True,
    ):
        self._lazy_initialized = False
        # noinspection PyTypeChecker
        CompletableGithubObject.__init__(
            self,
            requester=requester,
            headers=headers or {},
            attributes=attributes,
            completed=completed,
        )
        self._lazy_initialized = True
        self._lazy_requester = None

    @property
    def lazy_requester(self):
        if self._lazy_requester is None:
            app_auth = AppAuth(Event.app_id, os.getenv("PRIVATE_KEY"))
            token = (
                GithubIntegration(auth=app_auth)
                .get_access_token(Event.app_id)
                .token
            )
            Event.app_auth = app_auth
            self._lazy_requester = Requester(
                auth=Token(token),
                base_url=Consts.DEFAULT_BASE_URL,
                timeout=Consts.DEFAULT_TIMEOUT,
                user_agent=Consts.DEFAULT_USER_AGENT,
                per_page=Consts.DEFAULT_PER_PAGE,
                verify=True,
                retry=GithubRetry(),
                pool_size=None,
            )
        return self._lazy_requester

    def __getattribute__(self, item):
        """If the value is None, makes a request to update the object."""
        value = super().__getattribute__(item)
        if (
            not item.startswith("_lazy")
            and self._lazy_initialized
            and self._lazy_requester is None
            and value is None
        ):
            headers, data = self.lazy_requester.requestJsonAndCheck("GET", self.url)
            new_self = self.__class__(
                self.lazy_requester, headers, data, completed=True
            )
            self.__dict__.update(new_self.__dict__)
            value = super().__getattribute__(item)
        return value

    @staticmethod
    def get_lazy_instance(clazz, attributes):
        """Makes the clazz a subclass of LazyCompletableGithubObject"""
        if LazyCompletableGithubObject not in clazz.__bases__:
            clazz.__bases__ = tuple(
                [LazyCompletableGithubObject] + list(clazz.__bases__)
            )
        return clazz(attributes=attributes)
