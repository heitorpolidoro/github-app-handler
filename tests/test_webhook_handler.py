from unittest.mock import Mock, patch

from github import GithubIntegration
from github.Auth import AppUserAuth, Token

from githubapp import webhook_handler
from githubapp.webhook_handler import _get_auth
from tests.mocks import SubEventTest


def test_call_handler_sub_event(method, event_action_request):
    """
    Test the call handler sub event.

    Args:
        method: The method to be tested.
        event_action_request: The event action request.

    Raises:
        AssertionError: If the assertions fail.

    Example:
        test_call_handler_sub_event(method, event_action_request)
    """
    assert webhook_handler.webhook_handler(SubEventTest)(method) == method

    assert len(webhook_handler.handlers) == 1
    assert webhook_handler.handlers.get(SubEventTest) == [method]


def test_get_auth_app_user_auth(monkeypatch):
    monkeypatch.setenv("CLIENT_ID", "client_id")
    monkeypatch.setenv("CLIENT_SECRET", "client_secret")
    monkeypatch.setenv("TOKEN", "token")
    with patch(
        "githubapp.webhook_handler.AppUserAuth", autospec=AppUserAuth
    ) as appuserauth:
        assert isinstance(_get_auth(), AppUserAuth)
        appuserauth.assert_called_once_with(
            client_id="client_id", client_secret="client_secret", token="token"
        )


def test_get_auth_app_auth_when_private_key_in_env(monkeypatch):
    monkeypatch.setenv("PRIVATE_KEY", "private_key")

    get_access_token = Mock(return_value=Mock(token="token"))
    githubintegration = Mock(
        autospec=GithubIntegration, get_access_token=get_access_token
    )
    with (
        patch("githubapp.webhook_handler.AppAuth") as appauth,
        patch(
            "githubapp.webhook_handler.GithubIntegration",
            return_value=githubintegration,
            autospec=GithubIntegration,
        ) as GithubIntegrationMock,
        patch("githubapp.webhook_handler.Token", autospec=Token) as TokenMock,
    ):
        assert isinstance(
            _get_auth("hook_installation_target_id", "installation_id"), Token
        )
        appauth.assert_called_once_with("hook_installation_target_id", "private_key")
        GithubIntegrationMock.assert_called_once_with(auth=appauth.return_value)
        get_access_token.assert_called_once_with("installation_id")
        TokenMock.assert_called_once_with("token")
