import os
from typing import Any, Union
from unittest import mock
from unittest.mock import PropertyMock

from github.GithubObject import Attribute, CompletableGithubObject, NotSet

from githubapp.LazyCompletableGithubObject import LazyCompletableGithubObject


class LazyClass(CompletableGithubObject):
    def __init__(self, *args, **kwargs):
        self._url = Attribute
        self._url.value = "url"
        super().__init__(*args, **kwargs)

    def _initAttributes(self) -> None:
        self._attr1: Attribute[str] = NotSet

    def _useAttributes(self, attributes: dict[str, Any]) -> None:
        if "attr1" in attributes:  # pragma no branch
            self._attr1 = self._makeStringAttribute(attributes["attr1"])

    @property
    def attr1(self) -> Union[str, None]:
        self._completeIfNotSet(self._attr1)
        return self._attr1.value

    @staticmethod
    def url():
        return "url"


def test_lazy_attribute_access_initializes_requester():
    # Test that accessing an attribute on a LazyCompletableGithubObject triggers lazy initialization
    with mock.patch('githubapp.LazyCompletableGithubObject.Requester.requestJsonAndCheck') as mock_requestJsonAndCheck:
        mock_requestJsonAndCheck.side_effect = lambda *args, **kwargs: ({}, {'attr1': 'value1'})
        instance = LazyCompletableGithubObject.get_lazy_instance(LazyClass, attributes={})
        # Lazy initialization should fetch the correct value
        assert instance.attr1 == 'value1'
        # Requester should be initialized after access
        assert instance._requester._initialized
        mock_requestJsonAndCheck.assert_called_once_with('GET', instance.url())
    # Ensure a LazyCompletableGithubObject instance is initialized lazily
    instance = LazyCompletableGithubObject.get_lazy_instance(LazyClass, attributes={})
    assert isinstance(instance, LazyClass)
    assert not instance._requester._initialized  # Confirm requester is not initialized on instantiation
    # The assert not hasattr(instance, '_attr1') is removed as _attr1 is an attribute of LazyClass, to be tested with attribute access
    instance = LazyCompletableGithubObject.get_lazy_instance(LazyClass, attributes={})
    assert isinstance(instance, LazyClass)


def test_no_reinitialization_after_lazy_loading():
    # Test that after lazy initialization, the requester is not reinitialized on subsequent attribute access
    with mock.patch('githubapp.LazyCompletableGithubObject.LazyRequester') as MockLazyRequester:
        MockLazyRequester.return_value.requestJsonAndCheck.side_effect = [({'header':'value'}, {'attr1': 'value1'}), Exception('Requester should not be re-initialized')]
        instance = LazyCompletableGithubObject.get_lazy_instance(LazyClass, attributes={})
        # First attribute access triggers initialization
        _ = instance.attr1
        assert MockLazyRequester.return_value.requestJsonAndCheck.call_count == 1
        # Subsequent access should not reinitialize
        _ = instance.attr1
        assert MockLazyRequester.return_value.requestJsonAndCheck.call_count == 1
    # noinspection PyPep8Naming
    class MockRequester:
        @staticmethod
        def requestJsonAndCheck(*_args):
            return {}, {"attr1": "value1"}

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
        mock.patch.dict(os.environ, {"PRIVATE_KEY": "test-private-key"}, clear=True),
    ):
        instance = LazyCompletableGithubObject.get_lazy_instance(
            LazyClass, attributes={}
        )
        assert instance._attr1.value is None
        assert instance.attr1 == "value1"
        assert instance._attr1.value == "value1"

    app_auth.assert_called_once_with(123, "private-key")
