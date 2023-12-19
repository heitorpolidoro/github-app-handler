from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest

from githubapp import Flask, SignatureError
from githubapp.ReleaseEvent import ReleaseReleasedEvent


@pytest.fixture(autouse=True)
def event_mock(monkeypatch):
    event_mock_ = MagicMock()
    with patch("githubapp.Event", new=event_mock_):
        event_mock_.parse_event.return_value = ReleaseReleasedEvent
        yield event_mock_


class FlaskTest(TestCase):
    def setUp(self):
        app = Flask("testing")
        app._webhooks_ = {}
        app.testing = True
        self.app = app
        self.client = app.test_client()
        self.release_released = {
            "headers": {
                "X-Github-Hook-Id": "1",
                "X-Github-Event": "release",
                "X-Github-Delivery": "96940560-962a-11ee-9b3e-f1cfed967ee9",
                "X-Github-Hook-Installation-Target-ID": "684296",
                "X-Github-Hook-Installation-Target-Type": "integration",
            },
            "json": {
                "action": "released",
                "release": {},
                "repository": {},
                "sender": {},
                "installation": {"id": "1"},
            },
        }

    def test_root(self):
        response = self.client.get("/", **self.release_released)
        assert response.text == "testing App up and running!"

    def test_no_hooks(self):
        response = self.client.post("/", **self.release_released)

        self.assertEqual(response.status_code, 200)

    def test_event_handler_method_validation(self):
        with pytest.raises(SignatureError) as err:
            self.app.any(lambda: None)

        expected_message = (
            "Method FlaskTest.test_event_handler_method_validation.<locals>.<lambda>() "
            "signature error. The method must accept only one argument of the Event type"
        )
        assert str(err.value.message) == expected_message

    def test_call_any_event(self):
        called = False

        def method(_):
            nonlocal called
            called = True

        self.app.any(method)

        response = self.client.post("/", **self.release_released)

        self.assertEqual(response.status_code, 200)
        assert called

    def test_call_event(self):
        called = False

        def method(event):
            nonlocal called
            called = True

        self.app.Release(method)

        response = self.client.post("/", **self.release_released)

        self.assertEqual(response.status_code, 200)
        assert called

    def test_call_event_action(self):
        called = False

        def method(event):
            nonlocal called
            called = True

        self.app.ReleaseReleased(method)

        response = self.client.post("/", **self.release_released)

        self.assertEqual(response.status_code, 200)
        assert called

    def test_call_all(self):
        calls = 0

        def method(event):
            nonlocal calls
            calls += 1

        self.app.any(method)
        self.app.Release(method)
        self.app.ReleaseReleased(method)

        response = self.client.post("/", **self.release_released)

        self.assertEqual(response.status_code, 200)
        assert calls == 3

