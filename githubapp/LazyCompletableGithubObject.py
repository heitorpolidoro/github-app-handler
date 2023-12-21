import os
from typing import Any, Union

from github import Consts, GithubIntegration, GithubRetry
from github.Auth import AppAuth, Token
from github.GithubObject import CompletableGithubObject
from github.Requester import Requester

from githubapp.events import Event


class LazyRequester(Requester):
    def __init__(self):
        """
        Initialize the object.

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
        """
        Return the value of the named attribute of an object.

        Args:
            item (str): The name of the attribute to retrieve.

        Returns:
            Any: The value of the named attribute.

        Raises:
            AttributeError: If the named attribute does not exist.

        Example:
            # Create an instance of the class
            obj = MyClass()
            # Access a non-existent attribute
            try:
                value = obj.non_existent_attribute
            except AttributeError as e:
                print(e)
        """

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

        Example:
            To initialize the requester with authentication and default settings:
            ```
            requester = Requester()
            requester.initialize()
            ```

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
        """
        Initialize the object.

        Args:
            requester (Requester, optional): The requester object. Defaults to None.
            headers (dict[str, Union[str, int]], optional): The headers. Defaults to None.
            attributes (dict[str, Any], optional): The attributes. Defaults to None.
            completed (bool, optional): Indicates if the object is completed. Defaults to False.

        Raises:
            No specific exceptions are raised.

        Example:
            obj = ClassName(requester=Requester(), headers={"key": "value"}, attributes={"attr1": "value"}, completed=True)
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
        # self._lazy_initialized = True
        # self._lazy_requester = None
        self._requester = LazyRequester()

    # @property
    # def lazy_requester(self):
    #     if self._lazy_requester is None:
    #         self._lazy_requester = get_requester()
    #     return self._lazy_requester

    def __getattribute__(self, item):
        """
        If the value is None, makes a request to update the object.

        Args:
            item (str): The attribute being accessed.

        Returns:
            Any: The value of the attribute.

        Raises:
            <Exception Type>: <Description of the exception raised>

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
