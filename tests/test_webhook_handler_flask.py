from unittest import TestCase
from unittest.mock import MagicMock, Mock, call, patch

import pytest
from flask import Flask

from githubapp.webhook_handler import handle_with_flask


@pytest.fixture
def app():
    mock = MagicMock(spec=Flask)()
    mock.__class__ = Flask
    return mock


#     class Flask:
#         pass
#
#     mock_flask = MagicMock(name="Flask")
#     mock_flask_module = MagicMock(Flask=mock_flask)
#     mock_flask_module.Flask = Flask
#     sys.modules["flask"] = mock_flask_module
#     app = mock_flask()
#     app.__class__ = Flask
#     yield app


def test_handle_with_flask(app):
    handle_with_flask(app)
    assert app.route.call_count == 2
    app.route.assert_has_calls(
        [call("/", methods=["GET"]), call("/", methods=["POST"])], any_order=True
    )


def test_handle_with_flask_validation(app):
    class Other:
        pass

    app.__class__ = Other
    with pytest.raises(TypeError):
        handle_with_flask(app)
    assert app.route.call_count == 0


class TestApp(TestCase):
    def setUp(self):
        app = Flask("Test")
        handle_with_flask(app)
        self.app = app
        self.client = app.test_client()

    def test_root(self):
        """
        Test the root endpoint of the application.
        This test ensures that the root endpoint ("/") of the application is working correctly.
        It sends a GET request to the root endpoint and checks that the response status code is 200 and the response
        text is "Pull Request Generator App up and running!".
        """
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.text == "<h1>Test App up and running!</h1>"

    @staticmethod
    def test_root_not_default_index():
        app = Flask("Test")
        handle_with_flask(app, use_default_index=False)
        app.route("/", methods=["GET"])(lambda: "index")
        response = app.test_client().get("/")
        assert response.status_code == 200
        assert response.text == "index"

    @staticmethod
    def test_auth_callback():
        auth_callback = Mock()
        app = Flask("Test")
        handle_with_flask(app, auth_callback_handler=auth_callback)
        with patch("githubapp.webhook_handler.Github"):
            response = app.test_client().get("/auth-callback")
        assert response.status_code == 200
        auth_callback.assert_called_once()

    def test_webhook(self):
        """
        Test the webhook handler of the application.
        This test ensures that the webhook handler is working correctly.
        It mocks the `handle` function of the `webhook_handler` module, sends a POST request to the root endpoint ("/")
        with a specific JSON payload and headers, and checks that the `handle` function is called with the correct
        arguments.
        """
        with patch("githubapp.webhook_handler.handle") as mock_handle:
            request_json = {"action": "opened", "number": 1}
            headers = {
                "User-Agent": "Werkzeug/3.0.1",
                "Host": "localhost",
                "Content-Type": "application/json",
                "Content-Length": "33",
                "X-Github-Event": "pull_request",
            }
            self.client.post("/", headers=headers, json=request_json)
            mock_handle.assert_called_once_with(headers, request_json)
