import os
from datetime import timedelta
from typing import Any, Union
from unittest import mock
from unittest.mock import PropertyMock

import pytest
from dateutil.parser import parse
from github.GithubObject import Attribute, CompletableGithubObject, NotSet

from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class LazyClass(CompletableGithubObject):
    def __init__(self, *args, **kwargs):
        """
        Initialize the object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            None

        Example:
            obj = ClassName()
        """
        super().__init__(*args, **kwargs)

    def _initAttributes(self) -> None:
        self._attr1: Attribute[str] = NotSet
        self._url: Attribute[str] = NotSet

    def _useAttributes(self, attributes: dict[str, Any]) -> None:
        if "attr1" in attributes:  # pragma no branch
            self._attr1 = self._makeStringAttribute(attributes["attr1"])
        self._url = self._makeStringAttribute("url")

    @property
    def attr1(self) -> Union[str, None]:
        self._completeIfNotSet(self._attr1)
        return self._attr1.value


def test_lazy():
    instance = LazyCompletableGithubObject.get_lazy_instance(LazyClass, attributes={})
    assert isinstance(instance, LazyClass)


def test_lazy_requester_private_key():
    with (
        mock.patch("githubapp.LazyCompletableGithubObject.GithubIntegration"),
        mock.patch("githubapp.LazyCompletableGithubObject.AppAuth") as app_auth,
        mock.patch("githubapp.LazyCompletableGithubObject.Token"),
        mock.patch(
            "githubapp.LazyCompletableGithubObject.Requester._Requester__check",
            return_value=({}, {"attr1": "value1"}),
        ),
        mock.patch("githubapp.LazyCompletableGithubObject.Requester.requestJson"),
        mock.patch(
            "githubapp.LazyCompletableGithubObject.Event.hook_installation_target_id",
            new_callable=PropertyMock,
            return_value=123,
        ),
        mock.patch.dict(os.environ, {"PRIVATE_KEY": "private-key"}, clear=True),
    ):
        instance = LazyCompletableGithubObject.get_lazy_instance(
            LazyClass, attributes={}
        )
        assert instance._attr1.value is None
        assert instance.attr1 == "value1"
        assert instance._attr1.value == "value1"

    app_auth.assert_called_once_with(123, "private-key")


def test_lazy_requester_app_user_auth():
    os.environ["CLIENT_ID"] = "client_id"
    os.environ["CLIENT_SECRET"] = "client_secret"
    os.environ["TOKEN"] = "token"
    os.environ["REFRESH_TOKEN"] = "refresh_token"
    os.environ["DATE"] = "2023-12-31"
    date = parse(os.environ["DATE"])
    with (
        mock.patch("githubapp.LazyCompletableGithubObject.AppUserAuth") as app_use_auth,
        mock.patch(
            "githubapp.LazyCompletableGithubObject.Requester._Requester__check",
            return_value=({}, {"attr1": "value1"}),
        ),
        mock.patch("githubapp.LazyCompletableGithubObject.Requester.requestJson"),
    ):
        instance = LazyCompletableGithubObject.get_lazy_instance(
            LazyClass, attributes={}
        )
        assert instance._attr1.value is None
        assert instance.attr1 == "value1"
        assert instance._attr1.value == "value1"

    app_use_auth.assert_called_once_with(
        client_id="client_id",
        client_secret="client_secret",
        token="token",
        expires_at=date + timedelta(seconds=28800),
        refresh_token="refresh_token",
        refresh_expires_at=date + timedelta(seconds=15811200),
    )


def test_lazy_requester_attribute_error():
    with (
        mock.patch("githubapp.LazyCompletableGithubObject.GithubIntegration"),
        mock.patch("githubapp.LazyCompletableGithubObject.AppAuth"),
        mock.patch("githubapp.LazyCompletableGithubObject.Token"),
        mock.patch(
            "githubapp.LazyCompletableGithubObject.Requester._Requester__check",
            return_value=({}, {"attr1": "value1"}),
        ),
        mock.patch("githubapp.LazyCompletableGithubObject.Requester.requestJson"),
        mock.patch(
            "githubapp.LazyCompletableGithubObject.Event.hook_installation_target_id",
            new_callable=PropertyMock,
            return_value=123,
        ),
        mock.patch.dict(os.environ, {"PRIVATE_KEY": "private-key"}, clear=True),
    ):
        instance = LazyCompletableGithubObject.get_lazy_instance(
            LazyClass, attributes={}
        )
        with pytest.raises(AttributeError):
            # noinspection PyStatementEffect
            instance._requester.attr
