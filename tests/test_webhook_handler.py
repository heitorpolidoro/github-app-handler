from githubapp.webhook_handler import WebhookHandler, webhook_handler
from tests.mocks import EventTest, SubEventTest


def test_call_handler_sub_event(method, event_action_request):
    assert webhook_handler(SubEventTest)(method) == method

    assert len(WebhookHandler.handlers) == 1
    assert WebhookHandler.handlers.get(SubEventTest) == [method]
