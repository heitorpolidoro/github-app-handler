import os
from typing import Any, Union

from github import Consts, GithubIntegration, GithubRetry
from github.Auth import AppAuth, Token
from github.GithubObject import CompletableGithubObject
from github.Requester import Requester

from githubapp.events.event import Event


class LazyRequester(Requester):
    """
    This class is a lazy version of Requester, which means that it will not make any requests to the API
    until the object is accessed.
    When any attribute of Requester is accessed, initialize the requester.

    """

    def __init__(self):
        """
        Initializes the object.

        Args:
            self: The object itself.

        Raises:
            None

        Returns:
            None

        Example:
            obj = ClassName()
        """

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
        Requester.__init__(
            self,
            auth=Token(token),
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
        """
        Initialize the object.

        Args:
            requester (Requester, optional): The requester object. Defaults to None.
            headers (dict[str, Union[str, int]], optional): The headers dictionary. Defaults to None.
            attributes (dict[str, Any], optional): The attributes dictionary. Defaults to None.
            completed (bool, optional): Flag indicating if the object is completed. Defaults to False.

        Raises:
            None

        Example:
            obj = ClassName(requester=requester_obj, headers={"key": "value"}, attributes={"attr_key": "attr_value"}, completed=True)
        """

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

    def __getattribute__(self, item):
        """
        If the value is None, makes a request to update the object.

        Args:
            item (str): The attribute to retrieve.

        Returns:
            Any: The value of the attribute.

        Raises:
            <Exception Type>: Description of the exception raised.

        Example:
            # Usage example of __getattribute__
            value = obj.__getattribute__('attribute_name')
        """

        #     """If the value is None, makes a request to update the object."""
        value = super().__getattribute__(item)
        if value is None and item != "_requester" and not self._requester._initialized:
            headers, data = self._requester.requestJsonAndCheck("GET", self.url)
            self.__class__.__init__(
                self, self._requester, headers, data, completed=False
            )
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
