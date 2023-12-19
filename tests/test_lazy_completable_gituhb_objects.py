import os
from typing import Any, Union
from unittest import mock

from github.GithubObject import Attribute, CompletableGithubObject, NotSet

from github_app.LazyCompletableGithubObject import LazyCompletableGithubObject


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
        mock.patch("github_app.LazyCompletableGithubObject.GithubIntegration"),
        mock.patch("github_app.LazyCompletableGithubObject.AppAuth") as app_auth,
        mock.patch("github_app.LazyCompletableGithubObject.Token"),
        mock.patch(
            "github_app.LazyCompletableGithubObject.Requester",
            return_value=RequesterTest,
        ),
    ):
        assert instance._none_value.value is None
        assert instance.none_value == "none_value"
        assert instance._none_value.value == "none_value"

    app_auth.assert_called_once_with(123, None)
