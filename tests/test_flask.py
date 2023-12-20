# from collections import defaultdict
# from unittest import TestCase
# from unittest.mock import MagicMock, patch
#
# import pytest
#
# from githubapp import Flask
# from githubapp.Event import Event
# from githubapp.ReleaseEvent import ReleaseReleasedEvent
#
#
# @pytest.fixture(autouse=True)
# def event_mock(monkeypatch):
#     event_mock_ = MagicMock()
#     with patch("githubapp.Event", new=event_mock_):
#         event_mock_.parse_event.return_value = ReleaseReleasedEvent
#         yield event_mock_
#
#
from collections import defaultdict
from unittest import TestCase

import pytest

from githubapp.handlers.flask import Flask
from githubapp.webhook_handler import webhook_handler
from tests.mocks import SubEventTest


@pytest.fixture
def client():
    app = Flask("testing")
    app._webhooks = defaultdict(list)
    app.testing = True
    return app.test_client()


# class FlaskTest(TestCase):
#     def setUp(self):
#         self.app = app
#         self.client = app.test_client()
#         self.release_released = {
#             "headers": {
#                 "X-Github-Hook-Id": "1",
#                 "X-Github-Event": "release",
#                 "X-Github-Delivery": "96940560-962a-11ee-9b3e-f1cfed967ee9",
#                 "X-Github-Hook-Installation-Target-ID": "684296",
#                 "X-Github-Hook-Installation-Target-Type": "integration",
#             },
#             "json": {
#                 "action": "released",
#                 "release": {},
#                 "repository": {},
#                 "sender": {},
#                 "installation": {"id": "1"},
#             },
#         }
#
def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.text == "testing App up and running!"


def test_handle_webhook(client, method, event_action_request):
    webhook_handler(SubEventTest)(method)
    headers, json = event_action_request
    response = client.post("/", headers=headers, json=json)

    assert response.status_code == 200
    method.assert_called_once()


#
#     # def test_register_webhooks(self):
#     #     def func(_):
#     #         pass
#     #
#     #     def _register_all(event=Event):
#     #         for sub_event in event.__subclasses__():
#     #             if "Test" in sub_event.__name__:
#     #                 continue
#     #             event_name = sub_event.name
#     #             ret = getattr(self.app, event_name)(func)
#     #             assert (
#     #                 func == ret
#     #             ), f"Method {event_name} does not return the method itself"
#     #             assert sub_event in self.app._webhooks, f"{event_name} not registered"
#     #             self.app._webhooks = defaultdict(list)
#     #             _register_all(sub_event)
#     #
#     #     _register_all()
#
#     def test_no_hooks(self):
#         response = self.client.post("/", **self.release_released)
#
#         self.assertEqual(response.status_code, 200)
#
#     def test_call_any_event(self):
#         called = False
#
#         def method(_event):
#             nonlocal called
#             called = True
#
#         self.app.any(method)
#
#         response = self.client.post("/", **self.release_released)
#
#         self.assertEqual(response.status_code, 200)
#         assert called
#
#     def test_call_event(self):
#         called = False
#
#         def method(_event):
#             nonlocal called
#             called = True
#
#         self.app.release(method)
#
#         response = self.client.post("/", **self.release_released)
#
#         self.assertEqual(response.status_code, 200)
#         assert called
#
#     def test_call_event_action(self):
#         called = False
#
#         def method(_event):
#             nonlocal called
#             called = True
#
#         self.app.release.released(method)
#
#         response = self.client.post("/", **self.release_released)
#
#         self.assertEqual(response.status_code, 200)
#         assert called
#
#     def test_call_all(self):
#         calls = 0
#
#         def method(_event):
#             nonlocal calls
#             calls += 1
#
#         assert self.app.any(method) == method
#         assert self.app.release(method) == method
#         assert self.app.release.released(method) == method
#
#         response = self.client.post("/", **self.release_released)
#
#         self.assertEqual(response.status_code, 200)
#         assert calls == 3
