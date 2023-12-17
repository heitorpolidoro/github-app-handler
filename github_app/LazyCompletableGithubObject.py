import os
from typing import Any, Union

from github import Consts, GithubIntegration, GithubRetry
from github.Auth import AppAuth, Token
from github.GithubObject import CompletableGithubObject
from github.Requester import Requester

from github_app.Event import Event


class LazyCompletableGithubObject(CompletableGithubObject):
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
            token = (
                GithubIntegration(auth=AppAuth(681139, os.getenv("PRIVATE_KEY")))
                .get_access_token(Event.installation_id)
                .token
            )
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
        value = super().__getattribute__(item)
        if (
            not item.startswith("_lazy")
            and self._lazy_initialized
            and self._lazy_requester is None
            and value is None
        ):
            headers, data = self.lazy_requester.requestJsonAndCheck("GET", self.url)
            # parent_github_class = next(
            #     filter(
            #         lambda c: c != LazyCompletableGithubObject
            #                   and issubclass(c, CompletableGithubObject),
            #         self.__class__.__bases__,
            #     ),
            #     None,
            # )
            new_self = self.__class__(
                self.lazy_requester, headers, data, completed=True
            )
            # assert (
            #         self.url == new_self.url
            # ), f"{self.url} != {new_self.url}\n{self.lazy_requester.base_url=}"
            self.__dict__.update(new_self.__dict__)
            value = super().__getattribute__(item)
        return value

    @staticmethod
    def get_lazy_instance(cls, attributes):
        if LazyCompletableGithubObject not in cls.__bases__:
            cls.__bases__ = tuple([LazyCompletableGithubObject] + list(cls.__bases__))
        return cls(attributes=attributes)
        # return type(cls.__name__, (cls, LazyCompletableGithubObject), {})(
        #     attributes=attributes
        # )
