from githubapp.webhook_handler import webhook_handler, WebhookHandler
from tests.mocks import SubEventTest, EventTest


def test_call_handler_sub_event(method, event_action_request):
    assert webhook_handler(SubEventTest)(method) == method

    assert len(WebhookHandler.handlers) == 1
    assert WebhookHandler.handlers.get(SubEventTest) == [method]


