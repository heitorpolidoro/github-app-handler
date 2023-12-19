import os
from typing import Any, Union
from unittest import mock
from unittest.mock import PropertyMock

from github.GithubObject import Attribute, CompletableGithubObject, NotSet

from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class LazyClass(CompletableGithubObject):
    def __init__(self, *args, **kwargs):
        self._none_value = None
        super().__init__(*args, **kwargs)

    def _initAttributes(self) -> None:
        self._none_value: Attribute[str] = NotSet

    def _useAttributes(self, attributes: dict[str, Any]) -> None:
        if "none_value" in attributes:  # pragma no branch
            self._none_value = self._makeStringAttribute(attributes["none_value"])

    @property
    def none_value(self) -> Union[str, None]:
        self._completeIfNotSet(self._none_value)
        return self._none_value.value

    @staticmethod
    def url():
        return "url"


def test_lazy():
    instance = LazyCompletableGithubObject.get_lazy_instance(LazyClass, attributes={})
    assert isinstance(instance, LazyClass)


def test_lazy_requester():
    instance = LazyCompletableGithubObject.get_lazy_instance(LazyClass, attributes={})

    class RequesterTest:
        @staticmethod
        def requestJsonAndCheck(*_args):
            return {}, {"none_value": "none_value"}

    with (
        mock.patch("githubapp.LazyCompletableGithubObject.GithubIntegration"),
        mock.patch("githubapp.LazyCompletableGithubObject.AppAuth") as app_auth,
        mock.patch("githubapp.LazyCompletableGithubObject.Token"),
        mock.patch(
            "githubapp.LazyCompletableGithubObject.Requester",
            return_value=RequesterTest,
        ),
        mock.patch(
            "githubapp.LazyCompletableGithubObject.Event.app_id",
            new_callable=PropertyMock,
            return_value=123,
        ),
        mock.patch.dict(os.environ, {"PRIVATE_KEY": "private-key"}, clear=True),
    ):
        assert instance._none_value.value is None
        assert instance.none_value == "none_value"
        assert instance._none_value.value == "none_value"

    app_auth.assert_called_once_with(123, "private-key")
